import LineChartCard from "./LineChartCard.js";
import MyLineChart from "./LInechart_2.js";
import MyBarChart from "./MyBarChart.js";
import MyDonutChart from "./Pie_chart.js";

//<Navbar />

function App() {
  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Grid Layout for Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
        <MyLineChart />
        <MyBarChart />
        <LineChartCard />
        <MyDonutChart />
      </div>
    </div>
  );
}

export default App;
