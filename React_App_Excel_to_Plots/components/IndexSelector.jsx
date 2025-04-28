import React from "react";

const IndexSelector = ({ indices, selectedIndex, setSelectedIndex }) => {
  return (
    <div className="mt-4 w-full">
      <label className="block mb-2 text-white">Vegetation Index:</label>
      <select
        value={selectedIndex}
        onChange={(e) => setSelectedIndex(e.target.value)}
        className="w-full p-2 bg-gray-800 text-white border border-gray-700 rounded-lg"
      >
        <option value="">Select an index</option>
        {indices.map((index) => (
          <option key={index} value={index}>
            {index}
          </option>
        ))}
      </select>
    </div>
  );
};

export default IndexSelector;
