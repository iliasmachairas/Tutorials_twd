import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const ChartDisplay = ({ data, title }) => {
  if (data.length === 0) return null;

  return (
    <div className="mt-10 bg-gray-800 p-6 rounded-lg shadow-lg text-white">
      <h2 className="text-2xl font-semibold mb-6">{title}</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#444" />
          <XAxis dataKey="date" stroke="#aaa" />
          <YAxis stroke="#aaa" />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#4ade80"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartDisplay;
