import React from "react";

const PointSelector = ({
  points,
  selectedPoint,
  setSelectedPoint,
  resetIndexSelection,
}) => {
  return (
    <div className="w-full">
      <label className="block mb-2 text-white">Point:</label>
      <select
        value={selectedPoint}
        onChange={(e) => {
          setSelectedPoint(e.target.value);
          resetIndexSelection();
        }}
        className="w-full p-2 bg-gray-800 text-white border border-gray-700 rounded-lg"
      >
        <option value="">Select a point</option>
        {Object.keys(points).map((point) => (
          <option key={point} value={point}>
            {point}
          </option>
        ))}
      </select>
    </div>
  );
};

export default PointSelector;
