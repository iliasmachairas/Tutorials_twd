import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const data = [
  { name: "Jan", value: 400, secondaryValue: 320 },
  { name: "Feb", value: 300, secondaryValue: 280 },
  { name: "Mar", value: 500, secondaryValue: 470 },
  { name: "Apr", value: 200, secondaryValue: 210 },
  { name: "May", value: 350, secondaryValue: 330 },
];

const LineChartCard = () => {
  return (
    <div className="w-full max-w-4xl mx-auto p-4 bg-black rounded-2xl shadow-md border border-gray-300">
      <h2 className="text-2xl font-bold text-gray-700 mb-4 text-center">
        Monthly Performance
      </h2>
      <div className="w-full h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="value"
              name="Primary"
              stroke="#3B82F6"
              strokeWidth={3}
              activeDot={{ r: 8 }}
            />
            <Line
              type="monotone"
              dataKey="secondaryValue"
              name="Draft"
              stroke="#F97316"
              strokeDasharray="5 5"
              strokeWidth={2}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default LineChartCard;
