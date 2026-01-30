"use client";

import DropZone from "@/components/DropeZone";
import { useRef, useState } from "react";
import { FaArrowRight, FaFileAlt } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";

export default function Home() {
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [analysisType, setAnalysisType] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [filename, setFilename] = useState("");
  const fileInputRef = useRef(null);

  const types = ["aba", "boxes", "elemental"];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !analysisType) {
      alert("File or analysis type missing!");
      return;
    }
    setIsLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("filename", file.name);
    formData.append("analysisType", analysisType);
    setFilename(file.name.split(".")[0]);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload file");
      }

      // create a Blob URL for the download file
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      setDownloadUrl(downloadUrl);

      //clear the file input after report is processed
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = ""; // Reset the input field
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Loading Spinner */}
      {isLoading && (
        <div className="fixed inset-0 z-50 flex flex-col sm:flex-row items-center justify-center gap-4 backdrop-blur-md bg-black/30">
          <svg className="animate-spin h-8 w-8 text-white" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
          <span className="text-white text-lg font-semibold">
            Processing...
          </span>
        </div>
      )}

      <div className="flex min-h-screen flex-col items-center justify-center bg-slate-100 px-4 sm:px-8">
        <h1 className="mb-8 text-2xl md:text-4xl font-extrabold text-center">
          Static Tests Analysis
        </h1>
        <div className="flex w-full md:w-2/3 lg:w-1/3 flex-col rounded-md  bg-white p-6 sm:p-8 shadow-md">
          {/* Analysis Type */}
          <div className="pb-8 flex flex-col gap-4">
            <h2 className="text-lg font-bold text-slate-500">
              1. Select Analysis Type
            </h2>
            <ul className="flex flex-wrap justify-center gap-3">
              {types.map((type, index) => (
                <li
                  key={index}
                  className={`rounded-md shadow-md px-6 py-2 text-base sm:text-lg  cursor-pointer transition ${analysisType === type ? "border-2 border-blue-500 text-blue-500" : "border bg-slate-100 hover:border-blue-500 hover:text-blue-500 "}`}
                  onClick={() => setAnalysisType(type)}
                >
                  {type}
                </li>
              ))}
            </ul>
          </div>

          {/* File Upload */}
          <div className="flex flex-col gap-4">
            <h2 className="text-lg font-bold text-slate-500">
              2. Upload Your File
            </h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-6">
              <label htmlFor="file-upload" className="block cursor-pointer">
                <DropZone file={file} setFile={setFile} />
              </label>
              <input
                id="file-upload"
                type="file"
                className="hidden"
                onChange={(e) => setFile(e.target.files[0])}
              />
              <div className="flex justify-center">
                <button
                  type="submit"
                  className="flex w-full sm:w-auto items-center gap-3 rounded-md bg-blue-500 px-6 py-3 text-lg text-white shadow-lg transition hover:bg-blue-600 cursor-pointer"
                >
                  <span>Upload and Process</span>
                  <FaArrowRight className="text-base" />
                </button>
              </div>
            </form>
            {/* Download Section */}
            {downloadUrl && (
              <div className="mt-8 flex flex-col gap-4">
                <h2>Processed Report</h2>
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 rounded-md border border-black bg-slate-100 p-4">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="rounded-md bg-slate-50 p-3">
                      <FaFileAlt className="text-green-500" />
                    </div>
                    <span className="truncate font-medium">
                      {filename}.html
                    </span>
                  </div>

                  <a
                    className="flex items-center gap-2 font-bold text-blue-500 hover:underline"
                    href={downloadUrl}
                    download={`${filename}.html`}
                    onClick={() => setDownloadUrl("")}
                  >
                    <span>Download</span>
                    <IoMdDownload className="text-lg" />
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
