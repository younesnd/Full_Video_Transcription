import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: " AI-Powered Video Transcription & Translation App ",
  description: "AI-Powered Video Transcription & Translation App",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
