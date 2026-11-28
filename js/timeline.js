const margin = { top: 30, right: 40, bottom: 60, left: 70 };
const width = 900 - margin.left - margin.right;
const height = 450 - margin.top - margin.bottom;

const svg = d3.select("#timeline-chart")
    .html("")
    .append("svg")
    .attr("viewBox", `0 0 900 450`)
    .attr("width", "100%")
    .attr("height", "auto");

const chart = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

d3.csv("data/timeline.csv", d => ({
    date: d3.timeParse("%Y-%m-%d")(d["Report Date"]),
    amount: +d.Amount
})).then(data => {

    data = data.filter(d => d.date && Number.isFinite(d.amount));

    const x = d3.scaleTime()
        .domain(d3.extent(data, d => d.date))
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.amount) * 1.1])
        .nice()
        .range([height, 0]);

    chart.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    chart.append("g")
        .call(d3.axisLeft(y));

    const line = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.amount));

    chart.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "#34765a")
        .attr("stroke-width", 3)
        .attr("d", line);

    chart.append("text")
        .attr("x", width / 2)
        .attr("y", height + 50)
        .attr("text-anchor", "middle")
        .text("Date");

    chart.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", -50)
        .attr("text-anchor", "middle")
        .text("Average SO₂ emissions (lbs/hr)");

}).catch(error => console.error("Timeline error:", error));
