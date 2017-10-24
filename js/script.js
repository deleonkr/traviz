/* script.js 
   Author:
   Date:
*/


$(document).ready(function(){ // begin document.ready block

 // TIMETABLE
    
    var margin = { top: 60, right: 0, bottom: 70, left: 0 },
          width = 1024 - margin.left - margin.right,
          height = 430 - margin.top - margin.bottom,
          gridSize = Math.floor(width / 25),
          legendElementWidth = gridSize*2,
          buckets = 9,
          colors = ["#B4D81A","#FFE200","#FFC200","#FF9A00","#FF6D00","#FF3C00","#FF0000","#C10000"], // alternatively colorbrewer.YlGnBu[9]
          days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          times = ["Time", "12pm", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"];
          datasets = ["data/hourly_east-west.tsv", "data/hourly_west-east.tsv"];

    var svg = d3.select("#chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    /* ORIGINAL
            
    var dayLabels = svg.selectAll(".dayLabel")
        .data(days)
        .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", 0)
        .attr("y", function (d, i) { return i * gridSize; })
        .style("text-anchor", "end")
        .attr("transform", "translate(-6," + gridSize / 2 + ")")
        .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis");
        });
        
    var timeLabels = svg.selectAll(".timeLabel")
        .data(times)
        .enter().append("text")
        .text(function(d) { return d; })
        .attr("x", function(d, i) { return (i+1) * gridSize; })
        .attr("y", 0)
        .style("text-anchor", "middle")
        .attr("fill","#ffffff")
        .attr("transform", "translate(" + gridSize / 2 + ", -10)")
        .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });
        
    ORIGINAL */ 
    
    // STEFU
    
        var dayLabels = svg.selectAll(".dayLabel")
        .data(days)
        .enter().append("rect")
        .attr("x", 1)
        .attr("y", function (d, i) { return i * gridSize-4; })
        .attr("rx", 4)
        .attr("ry", 4)
        .style("text-anchor", "end")
        .attr("transform", "translate(-1," + 0 + ")")
        .attr("fill","#001E3C")
        .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis");
        });
    
        var dayLabels = svg.selectAll(".dayLabelText")
        .data(days)
        .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", gridSize/2)
        .attr("y", function (d, i) { return (i+1/2) * gridSize; })
        .style("text-anchor", "middle")
        .attr("transform", "translate(-1," + 0 + ")")
        .attr("class", function (d, i) { return ((i >= 0 && i <= 6) ? "dayLabelText mono axis axis-workweek" : "dayLabel mono axis");
        });
    
        var timeLabels = svg.selectAll(".timeLabel")
        .data(times)
        .enter().append("rect")
        .attr("x", function (d, i) { return i * gridSize+1; })
        .attr("y", -gridSize - 4)
        .attr("rx", 4)
        .attr("ry", 4)
        .style("text-anchor", "end")
        .attr("transform", "translate(-1," + 0 + ")")
        .attr("fill","#001E3C")
        .attr("class", function (d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis");
        });
        
        var timeLabels = svg.selectAll(".timeLabelText")
        .data(times)
        .enter().append("text")
        .text(function(d) { return d; })
        .attr("x", function(d, i) { return (i) * gridSize-1; })
        .attr("y", -10)
        .style("text-anchor", "middle")
        .attr("fill","#ffffff")
        .attr("transform", "translate(" + gridSize / 2 + ", -10)")
        .attr("class", function(d, i) { return ((i >= 26 && i <= 36) ? "timeLabelText mono axis axis-worktime" : "timeLabel mono axis"); });
    
        // STEFU */
    
        var heatmapChart = function(tsvFile) {
        d3.tsv(tsvFile,
        function(d) {
          return {
            day: +d.day,
            hour: +d.hour,
            value: +d.value
          };
        },
        function(error, data) {
          var datamin = d3.min(data, function (d) { return d.value; })
          var datamax = d3.max(data, function (d) { return d.value; })
          var colorScale = d3.scale.quantile()
              .domain([datamin,datamax])//d3.max(data, function (d) { return d.value; })
              .range(colors);
          
          var cards = svg.selectAll(".hour")
              .data(data, function(d) {return d.day+':'+d.hour;});

          cards.enter().append("rect")
              .attr("x", function(d) { return (d.hour+1) * gridSize; })
              .attr("y", function(d) { return (d.day-1) * gridSize -4; })
              .attr("rx", 4)
              .attr("ry", 4)
              .attr("class", "hour bordered")
              .attr("width", gridSize)
              .attr("height", gridSize)
              .style("fill", function(d) { return colorScale(d.value); });

          cards.transition().duration(1000)
              .style("fill", function(d) { return colorScale(d.value); });
          cards.exit().remove();


          var cardlabel = svg.selectAll(".timecost")
              .data(data, function(d) {return d.day+':'+d.hour;});

          cardlabel.enter().append("text")
              .text(function(d) {return null;})
              .attr("class", "timecost")
              .attr("text-anchor", "middle")
              .attr("x", function(d) { return (d.hour + 3/2) * gridSize; })
              .attr("y", function(d) { return (d.day - 1/2) * gridSize; })

          cardlabel.transition().duration(1000).text(function(d) {return d.value;})

          cardlabel.exit().remove();

          var legend = svg.selectAll(".legend")
              .data([0].concat(colorScale.quantiles()), function(d) { return d; });

          legend.enter().append("g")
              .attr("class", "legend");

          legend.append("rect")
            .attr("x", function(d, i) { return legendElementWidth * i+gridSize; })
            .attr("y", height)
            .attr("width", legendElementWidth)
            .attr("height", gridSize / 2)
            .style("fill", function(d, i) { return colors[i]; });

          legend.append("text")
            .attr("class", "mono")
            .text(function(d) { return "≥ " + Math.round(d); })
            .attr("x", function(d, i) { return legendElementWidth * i+gridSize; })
            .attr("y", height + gridSize);

          legend.exit().remove();

        });  
      };

      heatmapChart(datasets[0]);
      
      var datasetpicker = d3.select("#dataset-picker").selectAll(".table-button")
        .data(datasets);

      datasetpicker.enter()
        .append("input")
        .attr("value", function(d){ 
          if (d.indexOf("east-west") !== -1)
            {return "West to East";}
          else
            {return "East to West";}
        })
        .attr("type", "button")
        .attr("class", "table-button")
        .on("click", function(d) {
          heatmapChart(d);
        });
    
// TIMETABLE
    
        
}); //end document.ready block

