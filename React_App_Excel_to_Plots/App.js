import logo from "./logo.svg";
import "./App.css";
import FileUploader from "./components/FileUploader";
import PointSelector from "./components/PointSelector";
import IndexSelector from "./components/IndexSelector";
import * as XLSX from "xlsx";
import { useState } from "react";
import { useEffect } from "react";
import ChartDisplay from "./components/ChartDisplay";
import TailwindButton from "./components/TailwindButton";

function App() {
  const [points, setPoints] = useState({});
  const [selectedPoint, setSelectedPoint] = useState("");
  const [selectedIndex, setSelectedIndex] = useState("");
  const [chartData, setChartData] = useState([]);

  const handleFileUploaded = (file) => {
    const reader = new FileReader();

    reader.onload = (evt) => {
      const bstr = evt.target.result;
      const wb = XLSX.read(bstr, { type: "binary" });

      const sheetsData = {};
      wb.SheetNames.forEach((sheetName) => {
        const ws = wb.Sheets[sheetName];
        const data = XLSX.utils.sheet_to_json(ws, {
          header: 1,
          raw: false, // this line tells xlsx to parse dates instead of showing numbers
          dateNF: "yyyy-mm-dd", // you can customize the date format here
        });
        const headers = data[0];
        const rows = data.slice(1).map((row) => {
          const obj = {};
          headers.forEach((h, i) => {
            obj[h] = row[i];
          });
          return obj;
        });
        sheetsData[sheetName] = rows;
      });

      setPoints(sheetsData);
      console.log(setPoints);
    };

    reader.readAsBinaryString(file);
  };

  useEffect(() => {
    console.log("Points updated:", points);
  }, [points]);

  const handleLoadChart = () => {
    if (selectedPoint && selectedIndex) {
      const data = points[selectedPoint]?.map((item) => ({
        date: item["Date"] || item["date"], // adjust if needed
        value: item[selectedIndex],
      }));
      setChartData(data);
    }
  };

  const getIndices = () => {
    if (!selectedPoint || points[selectedPoint].length === 0) return []; // the second condition checks if there are columns for the point
    return Object.keys(points[selectedPoint][0]).filter(
      (k) => k.toLowerCase() !== "date"
    );
  };

  const resetIndexSelection = () => {
    setSelectedIndex("");
    setChartData([]);
  };

  useEffect(() => {
    console.log("Selected Point:", selectedPoint);
    console.log("Selected Index:", selectedIndex);
    console.log("Selected Index:", chartData);
  }, [selectedPoint, selectedIndex, chartData]);

  return (
    <div className="App bg-black text-white min-h-screen flex flex-col sm:flex-row justify-between p-6">
      <div className="w-full sm:w-1/3 flex flex-col items-center space-y-6">
        <FileUploader onFileUploaded={handleFileUploaded} />
        {Object.keys(points).length > 0 && (
          <div className="w-full">
            <PointSelector
              points={points}
              selectedPoint={selectedPoint}
              setSelectedPoint={setSelectedPoint}
              resetIndexSelection={resetIndexSelection}
            />

            {selectedPoint && (
              <>
                <IndexSelector
                  indices={getIndices()}
                  selectedIndex={selectedIndex}
                  setSelectedIndex={setSelectedIndex}
                />
                <div className="mt-4">
                  <button
                    onClick={handleLoadChart}
                    disabled={!selectedIndex}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg disabled:bg-gray-500 transition-all"
                  >
                    Load Chart
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </div>

      <div className="w-full sm:w-2/3 flex-grow mt-6 sm:mt-0">
        <ChartDisplay
          data={chartData}
          title={
            selectedPoint && selectedIndex
              ? `${selectedPoint} - ${selectedIndex}`
              : ""
          }
        />
      </div>
    </div>
  );
}

export default App;
