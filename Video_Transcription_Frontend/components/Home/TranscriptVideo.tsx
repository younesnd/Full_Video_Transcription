"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Spinner } from "../ui/spinner";
import { API_BASE_URL, SUPPORTED_LANGUAGES } from "@/constant/constant";
import type { UploadResponse, PollingResponse } from "@/types/types";

const TranscriptVideo = () => {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState<string>("en");
  const [uploadId, setUploadId] = useState<string | null>(null);
  const [translation, setTranslation] = useState<string>("");
  const [status, setStatus] = useState<
    "in-progress" | "success" | "error" | ""
  >("");
  const [error, setError] = useState<string | null>(null);
  const [isPolling, setIsPolling] = useState<boolean>(false);

  const handleUpload = async (): Promise<void> => {
    setError(null);
    setTranslation("");
    setStatus("");
    setUploadId(null);

    if (!file) {
      setError("Please select a valid MP4 file to upload.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("target_language", language);

      const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || "Upload failed due to server error.");
      }

      const data: UploadResponse = await response.json();
      setUploadId(data.job_id);
      setStatus("in-progress");
      setIsPolling(true);
    } catch (err: unknown) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "Unexpected error occurred during upload.";
      setError(errorMessage);
    }
  };

  useEffect(() => {
    if (!uploadId || !isPolling) return;

    const startTime = Date.now();
    const POLL_TIMEOUT = 60_000;

    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/${uploadId}`);
        if (!response.ok) throw new Error("Failed to poll job status.");

        const data: PollingResponse = await response.json();
        setStatus(data.status);

        if (data.status === "success") {
          setTranslation(data.translation || "");
          setIsPolling(false);
          clearInterval(interval);
        } else if (data.status === "error") {
          setError("An error occurred during transcription or translation.");
          setIsPolling(false);
          clearInterval(interval);
        }

        if (Date.now() - startTime > POLL_TIMEOUT) {
          setError("Request timed out. Please try again later.");
          setIsPolling(false);
          clearInterval(interval);
        }
      } catch (err: unknown) {
        const errorMessage =
          err instanceof Error ? err.message : "Polling error occurred.";
        setError(errorMessage);
        setIsPolling(false);
        clearInterval(interval);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [uploadId, isPolling]);

  return (
    <main className="max-w-2xl mx-auto mt-12 p-8 border border-gray-200 rounded-2xl shadow-md bg-white space-y-6">
      <h1 className="text-3xl font-semibold text-gray-800">
        🎥 Video Transcription & Translation
      </h1>

      <div className="space-y-2">
        <Label htmlFor="video" className="text-sm text-gray-600">
          Upload MP4 Video
        </Label>
        <Input
          id="video"
          type="file"
          accept="video/mp4"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setFile(e.target.files?.[0] || null)
          }
          className="cursor-pointer border-dashed border-2 border-gray-300 hover:border-blue-500"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="language" className="text-sm text-gray-600">
          Target Language
        </Label>
        <Select
          value={language}
          onValueChange={(val: string) => setLanguage(val)}
        >
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select a language" />
          </SelectTrigger>
          <SelectContent>
            {SUPPORTED_LANGUAGES.map(({ label, value }) => (
              <SelectItem key={value} value={value}>
                {label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <Button
        className="w-full text-md"
        onClick={handleUpload}
        disabled={isPolling}
      >
        {isPolling ? "Processing..." : "Upload & Translate"}
      </Button>

      {error && (
        <div className="p-4 mt-4 bg-red-100 text-red-700 border border-red-300 rounded-md text-sm">
          ⚠️ {error}
        </div>
      )}

      {status && !error && (
        <div className="pt-4 border-t mt-6 space-y-4">
          <div className="flex items-center gap-2 text-sm text-gray-700">
            <span className="font-medium">Status:</span>
            <span
              className={`capitalize ${
                status === "success"
                  ? "text-green-600"
                  : status === "error"
                  ? "text-red-600"
                  : "text-blue-600"
              }`}
            >
              {status}
            </span>
            {status === "in-progress" && (
              <Spinner className="text-blue-500 w-4 h-4" />
            )}
          </div>

          {translation && (
            <div className="p-4 bg-gray-50 border rounded-md overflow-auto max-h-64">
              <h2 className="text-sm font-medium mb-2 text-gray-700">
                Translation Output:
              </h2>
              <pre className="whitespace-pre-wrap text-sm text-gray-800">
                {translation}
              </pre>
            </div>
          )}
        </div>
      )}
    </main>
  );
};

export default TranscriptVideo;
