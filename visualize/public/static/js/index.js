import * as d3 from "https://cdn.skypack.dev/d3@7";
import axios from "https://cdn.skypack.dev/axios";

const dataSet = async function getData() {
  return await axios.get("/api/markov-chain");
};
async function drawChart() {
  const resp = await dataSet();

  const data = resp.data;

  const ARROWSIZE = 10; 
  const STRENGTH = -1000; 
  const RADIUS = 10; 
  const NODE_COLOR = "#999";
  const LINK_COLOR = "#999";

  const svgWidth = 500;
  const svgHeight = 500;
  const barPadding = 5;
  const barWidth = svgWidth / data.length;

  const width = 928;
  const height = 600;

  // Specify the color scale.
  const color = d3.scaleOrdinal(d3.schemeCategory10);

  // The force simulation mutates links and nodes, so create a copy
  // so that re-evaluating this cell produces the same result.
  const links = data.links.map((d) => ({ ...d }));
  const nodes = data.nodes.map((d) => ({ ...d }));
  const maxLinkValue = Math.max(...links.map((d) => d.value));

  // Create a simulation with several forces.
  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3.forceLink(links).id((d) => d.id)
    )
    .force("charge", d3.forceManyBody().strength(STRENGTH))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .on("tick", ticked);

  // Create the SVG container.

  let svg = d3.select("svg");

  svg
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;");

  svg
    .append("defs")
    .append("marker")
    .attr("id", "arrowhead")
    .attr("viewBox", "-0 -5 10 10")
    .attr("orient", "auto")
    .attr("refX", 20)
    .attr("refY", 0)
    .attr("markerWidth", ARROWSIZE)
    .attr("markerHeight", ARROWSIZE)
    .attr("xoverflow", "visible")
    .append("svg:path")
    .attr("d", "M 0,-5 L 10 ,0 L 0,5")
    .attr("fill", "999")
    .style("stroke", "none");

  // Add a line for each link, and a circle for each node.
  const link = svg
    .append("g")
    .attr("id", "arrow")
    .attr("stroke", LINK_COLOR)
    .selectAll()
    .data(links)
    .join("line")
    .attr("stroke-width", (d) => d.value / maxLinkValue *5)
    .attr("stroke-opacity",(d) => (d.value / maxLinkValue)*5)
    .attr("marker-end", "url(#arrowhead)"); // reference the marker here

  const node = svg
    .append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll()
    .data(nodes)
    .join("circle")
    .attr("r", RADIUS)
    .attr("fill", NODE_COLOR);

  node.append("title").text((d) => d.id);

  // Create text labels
  const label = svg
    .append("g")
    .selectAll("text")
    .data(nodes)
    .join("text")
    .text((d) => d.id) // replace d.id with the property you want to display
    .attr("dx", -1) // dx and dy are offsets from the circle's center
    .attr("dy", 0);

  // Add a drag behavior.
  node.call(
    d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended)
  );

  // Set the position attributes of links and nodes each time the simulation ticks.
  function ticked() {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
    label.attr("x", (d) => d.x).attr("y", (d) => d.y);
  }

  // Reheat the simulation when drag starts, and fix the subject position.
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  // Update the subject (dragged node) position during drag.
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  // Restore the target alpha so the simulation cools after dragging ends.
  // Unfix the subject position now that it’s no longer being dragged.
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
}
drawChart();
