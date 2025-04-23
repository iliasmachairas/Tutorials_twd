import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

const sampleData = [
  { name: 'Page A', uv: 400 },
  { name: 'Page B', uv: 300 },
  { name: 'Page C', uv: 500 },
];

const MyLineChart = () => {
  return (
    <div className="w-full max-w-4xl mx-auto p-4 bg-black rounded-2xl shadow-md border border-gray-300">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">User Visits Over Pages</h2>
      <div className="w-full h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={sampleData}>
            <CartesianGrid stroke="#e5e7eb" strokeDasharray="5 5" />
            <XAxis dataKey="name" tick={{ fill: '#6b7280' }} />
            <YAxis tick={{ fill: '#6b7280' }} />
            <Tooltip contentStyle={{ backgroundColor: '#fff', borderColor: '#ddd' }} />
            <Line type="monotone" dataKey="uv" stroke="#6366f1" strokeWidth={3} dot={{ r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MyLineChart;
