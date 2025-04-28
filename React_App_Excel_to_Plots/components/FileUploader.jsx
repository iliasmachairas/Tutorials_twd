import React from "react";

const FileUploader = ({ onFileUploaded }) => {
  const handleFile = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log(file);
      onFileUploaded(file);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-gray-800 rounded-2xl shadow-md border border-gray-700 w-full max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-white mb-4">Upload Excel File</h2>
      <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-blue-500 rounded-lg cursor-pointer hover:bg-blue-600 transition">
        <div className="flex flex-col items-center justify-center pt-3 pb-4">
          <p className="mb-1 text-sm text-gray-300 font-semibold">
            Click to upload or drag and drop
          </p>
          <p className="text-xs text-gray-500">Only .xlsx or .xls files</p>
        </div>
        <input
          type="file"
          className="hidden"
          accept=".xlsx, .xls"
          onChange={handleFile}
        />
      </label>
    </div>
  );
};

export default FileUploader;
