function drawmap(){
	var width = 1366, height = 700;
	//创建svg
	var svg = d3.select("body")
		.append("svg")
		.attr("width", width)
		.attr("height", height);
	//设置投影
	var projection = d3.geo.mercator()
		.translate([width / 2, height / 2])
		.center([105, 38]).scale(800);
	//创建path
	var path = d3.geo.path().projection(projection);
	var g = svg.append('g').call(d3.behavior.zoom()
		.scaleExtent([1, 50])
		.on("zoom", zoom));

	var color = d3.scale.category20();


	//解析json并绑定
	d3.json("http://oe3hv1l98.bkt.clouddn.com/china.geo.json", 
		function(json){
		console.log(json.features)
		g.selectAll("path")
			.data(json.features)
			.enter().append("path")
			.attr("d", path)
			.attr('fill', 'rgba(204,204,204,0.81)')
	        .attr('stroke', 'rgba(204,255,255,1)')
	        .attr('stroke-width', 1)
	        .on("mouseover",function(d,i){
                d3.select(this)
                    .attr("fill",'rgba(0,204,255,0.61)');
            })
            .on("mouseout",function(d,i){
                d3.select(this)
                    .attr("fill",'rgba(204,204,204,0.81)');
            });
	    for (var i = json.features.length - 1; i >= 0; i--) {
	    	geo = json.features[i]['properties']['cp']
	    	name = json.features[i]['properties']['name']
	    	g.append("text")
	    		.attr("x",projection(geo)[0] - 8)
				.attr("y",projection(geo)[1] + 8)
				.attr("fill", function(d, i){ return color(i)})
				.attr("font-size", 8)
				.html(name)
	    }
		
	});

	d3.json("http://localhost:8000/population", function(json){
		info = json.data
		for (var i = info.length - 1; i >= 0; i--) {
			city = info[i][0]
			lat = info[i][1]
			lon = info[i][2]
			count = info[i][3]
			count_rate = count / 100
			geo = [lat, lon]
			g.append("circle")
				.attr("cx", projection(geo)[0])
				.attr("cy", projection(geo)[1])
				.attr("r", count_rate)
				.attr("fill", "rgba(51,153,255,0.6)")
				.attr("attr-city", city)
				.attr("attr-count", count)
				.attr("attr-x", projection(geo)[0])
				.attr("attr-y", projection(geo)[1])
				.on("mouseover", function(){
					city = d3.select(this).attr("attr-city")
					count = d3.select(this).attr("attr-count")
					x = d3.select(this).attr("attr-x")
					y = d3.select(this).attr("attr-y")
					g.append("g").append("text")
						.attr("x", x)
						.attr("y", y)
						.attr("font-size", 12)
						.attr("fill", "rgba(66,66,66,0.8)")
						.html(city + '/' + count + '万人');
				}).on("mouseout", function(){
					d3.select("g").selectAll("g").remove();
				})
		}
	})

	d3.json("http://localhost:8000/",
		function(json){
		info = json.data
		for (var i = info.length - 1; i >= 0; i--) {
			price = parseInt(info[i][4])
			price_rate = price / 3000
			geo_list = [info[i][2], info[i][3]]
			g.append("circle")
				.attr("cx",projection(geo_list)[0])
				.attr("cy",projection(geo_list)[1])
				.attr("attr-city", info[i][1])
				.attr("attr-price", price)
				.attr("r", price_rate)
				.attr("fill", "rgba(255,0,102,0.6)")
				.on("mouseover", function(){
					x = d3.select(this).attr("cx");
					y = d3.select(this).attr("cy");
					price = d3.select(this).attr("attr-price");
					city = d3.select(this).attr("attr-city");
					g.append("g").append("text")
						.attr("x", x)
						.attr("y", y)
						.attr("font-size", 12)
						.attr("fill", "rgba(66,66,66,0.8)")
						.html(city + '/' + price + '元/㎡');
				}).on("mouseout", function(){
					d3.select("g").selectAll("g").remove();
				});
			
		}
	});

	function zoom(){
		g.attr("transform", "translate(" + 
			d3.event.translate + ")scale(" +
			d3.event.scale +")");
	}
}


