$(function() {
    // Set the dimensions of the canvas and graph.
    var margin = {top: 30, right: 20, bottom: 70, left: 50},
    width = 1000 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    // Parse the date and time.
    var parseDate = d3.timeParse("%b %Y");

    // Set the ranges
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // Define the axes
    var xAxis = d3.axisBottom(x).ticks(5);
    var yAxis = d3.axisLeft(y).ticks(5);

    // Define the line
    var priceline = d3.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.price); });

    // Adds the svg canvas
    var svg = d3.select("#chart")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", 
                  "translate(" + margin.left + "," + margin.top + ")");

    // Get the data
    // Notice: D3 5.x uses promises instead of Ajax calls.
    d3.csv("static/stocks.csv").then(function(data) {
        data.forEach(function(d) {
            d.date = parseDate(d.date);
            d.price = +d.price;
        });

        // Scale the range of the data.
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0, d3.max(data, function(d) { return d.price; })]);

        // Nest the entries by symbol.
        var dataNest = d3.nest()
            .key(function(d) {return d.symbol;})
            .entries(data);

        // set the color scale.
        var color = d3.scaleOrdinal(d3.schemeCategory10); 

        // Set spacing for the legend.
        var legendSpace = width / dataNest.length; 

        // Loop through each symbol and key.
        dataNest.forEach(function(d, i) { 

            // Add the lines to the chart.
            svg.append("path")
                    .attr("class", "line")
                    .style("stroke", function() { 
                            return d.color = color(d.key); 
                    })
                    .attr("id", 'tag'+d.key.replace(/\s+/g, '')) // assign ID
                    .attr("d", priceline(d.values));

            // Add the Legend
            svg.append("text")
                .attr("x", (legendSpace / 2) + i * legendSpace)  
                .attr("class", "legend")   
                .style("fill", function() { 
                    return d.color = color(d.key); 
                })
                .on("click", function() {
                        // Determine if current line is visible 
                        var active   = d.active ? false : true,
                        newOpacity = active ? 0 : 1;

                        // Hide or show the elements based on the ID
                        d3.select("#tag"+d.key.replace(/\s+/g, ''))
                            .transition().duration(100) 
                            .style("opacity", newOpacity); 

                        // Update whether or not the elements are active
                        d.active = active;
                })  
                .text(d.key); 

        });

        // Add the X axis.
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the Y axis.
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);
    });
});
