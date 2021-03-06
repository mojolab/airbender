

function getSiPm25(pm25){
	//console.log("PM25: "+pm25)
	if(pm25<=30){
		return pm25*50/30
	}
	else if(pm25>30 && pm25<=60){
		return 50+(pm25-30)*50/30;
	}
	else if(pm25>60 && pm25<=90){
		return 100+(pm25-60)*100/30;
	}				
	else if(pm25>90 && pm25<=120){
		return 200+(pm25-90)*(100/30);
	}
	else if(pm25>120 && pm25<=250){
		return 300+(pm25-120)*(100/130);
	}
	else if(pm25>250){
		return 400+(pm25-250)*(100/130);
	}

}
function getSiPm10(pm10){
	//console.log("PM10: "+pm10)
	if(pm10<=50){
		return pm10
	}
	else if(pm10>50 && pm10<=100){
		return pm10
	}
	else if(pm10>100 && pm10<=250){
		return 100+(pm10-100)*100/150;
	}
	else if(pm10>250 && pm10<=350){
		return 200+(pm10-250);
	}
	else if(pm10>350 && pm10<=430){
		return 300+(pm10-350)*(100/80);
	}
	else if(pm10>430){
		return 400+(pm10-430)*(100/80);
	}
}
		


//Functions to calculate aqi
		
		
function getLatestAvgs(id,channeldata){
		channeldata=channeldata.slice(-10)
		//console.log(channeldata)
		sumsipm25=0.0
		sumsipm10=0.0
		sumaqi=0.0
		sumpm10=0
		sumpm25=0
		for (row in channeldata){
			
			pm25=parseFloat(channeldata[row].pm25)
			if (pm25==NaN){
				console.log(channeldata)
			}
			
			pm10=parseFloat(channeldata[row].pm10)
			sumpm10=sumpm10+pm10
			sumpm25=sumpm25+pm25
			sipm25=getSiPm25(pm25)
			if (sipm25==NaN){
				console.log(channeldata)
			}
			sipm10=getSiPm10(pm10)
			sumsipm10=sumsipm10+sipm10
			sumsipm25=sumsipm25+sipm25
			if(sipm10>sipm25){
				aqi=sipm10;
			}
			else{
				aqi=sipm25;
			}
			//console.log("PM10:"+pm10+" SIPM10:"+sipm10+" PM25: "+pm25+" SIPM25:"+sipm25+" AQI: "+aqi)
			sumaqi=sumaqi+aqi
			ts=channeldata[row].created_at
		}
		ts=channeldata[row].created_at
		
		avgsipm25=sumsipm25/10
		avgsipm10=sumsipm10/10
		avgaqi=sumaqi/10
		avgpm10=sumpm10/10
		avgpm25=sumpm25/10
		response={}
		response['avgaqi']=Math.round(avgaqi)
		response['avgsipm25']=Math.round(avgsipm25)
		response['avgsipm10']=Math.round(avgsipm10)
		response['avgpm10']=Math.round(avgpm10)
		response['avgpm25']=Math.round(avgpm25)
		response['ts']={"date":ts.split("T")[0],"time":ts.split("T")[1].split("Z")[0]}
		return response
}


function displayGraph(div,data=null){
	//console.log(div)
	parseTime=d3.timeParse("%Y-%m-%dT%H:%M:%SZ")
	//console.log(parseTime(data[0]['created_at']))
	//console.log(data[0]['created_at'])
	gheight=130
	//pm10={height: $("#pm10").height(), width:$("#pm10").width()}
	//aqi={height: $("#aqi").height(), width:$("#aqi").width()}
	//pm25={height: $("#pm25").height(), width:$("#pm25").width()}
	pm10={height: gheight, width:$("#pm10").width()}
	aqi={height: gheight, width:$("#aqi").width()}
	pm25={height: gheight, width:$("#pm25").width()}
	
	var svgpm25 = d3.select(div).select('#pm25').append("svg")
								.attr("width",pm25.width)
								.attr("height",pm25.height)
								.attr("id", "svgpm25")
		
	var svgpm10 = d3.select(div).select('#pm10').append("svg")
								.attr("width",pm10.width)
								.attr("height",pm10.height)
								.attr("id", "svgpm10")
	
	var svgaqi = d3.select(div).select('#aqi').append("svg")
								.attr("width",aqi.width)
								.attr("height",aqi.height)
								.attr("id", "svgaqi")
		
	//console.log(d3.time.hour.floor(new Date()))
	//console.log(d3.time.hour.ceil(new Date()))
		
	var x = d3.scaleTime().range([0, pm10.width-40]);  
	var y = d3.scaleLinear().range([gheight-25, 0]);


	height=gheight-25
	
	data.forEach(function(d) {
		d.created_at = parseTime(d.created_at);
		d.pm10 = +d.pm10;
		d.pm25 = +d.pm25;
		d.sipm10=Math.round(getSiPm10(d.pm10));
		d.sipm25=Math.round(getSiPm25(d.pm25));
		if(d.sipm10>d.sipm25){
			d.aqi=d.sipm10;
		}
		else{
			d.aqi=d.sipm25;
		}
		d.aqi = +d.aqi;
		
    });
    //console.log(data)
    x.domain(d3.extent(data, function(d) { return d.created_at; }));
    y.domain([0, d3.max(data, function(d) { return d.aqi; })]);
	// Define the line
	
	svgpm10=d3.select(div).select("#svgpm10").append("g")
	
	pm10line=d3.line()
    .x(function(d) { return x(d.created_at); })
    .y(function(d) { return y(d.pm10); });

	pm25line=d3.line()
    .x(function(d) { return x(d.created_at); })
    .y(function(d) { return y(d.pm25); });

	aqiline=d3.line()
    .x(function(d) { return x(d.created_at); })
    .y(function(d) { return y(d.aqi); });

	
	d3.select(div).select("#svgpm10")			
		.append("g")
		.attr("transform","translate(30,0)")
		.append("path")
		.datum(data)
			.attr("fill", "none")
			.attr("stroke", "steelblue")
			.attr("stroke-linejoin", "round")
			.attr("stroke-linecap", "round")
			.attr("stroke-width", 1.5)
			.attr("d", pm10line);
		
		
	d3.select(div).select("#svgpm25")			
		.append("g")
		.attr("transform","translate(30,0)")
		.append("path")
		.datum(data)
			.attr("fill", "none")
			.attr("stroke", "orange")
			.attr("stroke-linejoin", "round")
			.attr("stroke-linecap", "round")
			.attr("stroke-width", 1.5)
			.attr("d", pm25line);
	
	
	d3.select(div).select("#svgaqi")			
		.append("g")
		.attr("transform","translate(30,0)")
		.append("path")
		.datum(data)
			.attr("fill", "none")
			.attr("stroke", "red")
			.attr("stroke-linejoin", "round")
			.attr("stroke-linecap", "round")
			.attr("stroke-width", 1.5)
			.attr("d", aqiline);
	
	
	
	d3.select(div).select("#svgpm10")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(30," + height + ")")
		.call(d3.axisBottom(x)
              .tickFormat(d3.timeFormat("%H:%M"))
              .ticks(4))
      .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-35)");
    
    
    d3.select(div).select("#svgpm10")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(30,0)")
		.call(d3.axisLeft(y)
				.ticks(4))
	  .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-45)");

	d3.select(div).select("#svgpm25")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(30," + height + ")")
		.call(d3.axisBottom(x)
              .tickFormat(d3.timeFormat("%H:%M")))
      .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-35)");

	 d3.select(div).select("#svgpm25")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(30,0)")
		.call(d3.axisLeft(y)
				.ticks(4))
	  .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-45)");
		
	d3.select(div).select("#svgaqi")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(30," + height + ")")
		.call(d3.axisBottom(x)
              .tickFormat(d3.timeFormat("%H:%M")))
      .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-35)");
        
    d3.select(div).select("#svgaqi")			
		.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(30,0)")
		.call(d3.axisLeft(y)
				.ticks(4))
	  .selectAll("text")	
        .style("text-anchor", "end")
        .attr("dx", "-.08em")
        .attr("dy", ".075em")
        .attr("transform", "rotate(-45)");

}
