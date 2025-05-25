
export type UploadResponse = {
  job_id: string;
};

export type PollingResponse = {
  status: "in-progress" | "success" | "error";
  translation?: string;
};
