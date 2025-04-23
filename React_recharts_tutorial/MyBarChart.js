import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const sampleBarData = [
  { name: 'Page A', clicks: 240, impressions: 500, conversions: 30 },
  { name: 'Page B', clicks: 138, impressions: 420, conversions: 22 },
  { name: 'Page C', clicks: 340, impressions: 800, conversions: 47 },
  { name: 'Page D', clicks: 290, impressions: 610, conversions: 35 },
  { name: 'Page E', clicks: 200, impressions: 300, conversions: 18 },
];

const MyBarChart = () => {
  return (
    <div className="w-full max-w-4xl mx-auto p-4 bg-black rounded-2xl shadow-md border border-gray-300">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Page Performance Overview</h2>
      <div className="w-full h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={sampleBarData} barGap={10}>
            <CartesianGrid stroke="#e5e7eb" strokeDasharray="4 4" />
            <XAxis dataKey="name" tick={{ fill: '#6b7280' }} />
            <YAxis tick={{ fill: '#6b7280' }} />
            <Tooltip contentStyle={{ backgroundColor: '#fff', borderColor: '#ddd' }} />
            <Legend />
            <Bar dataKey="clicks" fill="#6366f1" radius={[6, 6, 0, 0]} />
            <Bar dataKey="impressions" fill="#34d399" radius={[6, 6, 0, 0]} />
            <Bar dataKey="conversions" fill="#f59e0b" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MyBarChart;
