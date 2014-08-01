$(function() {
    $( "#draggable" ).draggable();
});

var w = 750;
h = 750;
links = [];
nodes = {};
var data;
d3.csv("data/patcitation.csv", function(data) {
    data.forEach(function(d) {
        links.push({'source': d.source, 'target': d.target});
    })

    links.forEach(function(link) {
        link.source = (nodes[link.source] || (nodes[link.source] = {name: link.source, ref:0}));
        link.target = (nodes[link.target] || (nodes[link.target] = {name: link.target, ref:0}));
        nodes[link.target.name].ref = nodes[link.target.name].ref + 1;
    })
})

d3.json("data/patinfo.json", function (error, json) {
    if (error) return console.warn(error);
    data=json;
    data.forEach(function(d) {
        node = nodes[d.Patent];
        node['GYear'] = d.GYear;
        node['PClass'] = d.PClass;
        node['Firstname'] = d.Firstname;
        node['Lastname'] = d.Lastname;
        node['Street'] = d.Street;
        node['State'] = d.State;
        node['Country'] = d.Country;
        node['Zipcode'] = d.Zipcode;
    })

    var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(links)
    .size([w,h])
    .linkDistance(90)
    .charge(-500)
    .on("tick", tick)
    .start();

    var svg = d3.select("body").append("svg:svg")
        .attr("width", w)
        .attr("heigth", h);

    svg.append("svg:defs").append("svg:marker")
        .attr("id", "end-arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15) //15
        .attr("refY", -1.5) // -1.5
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("svg:path")
        .attr("d", "M0, -5L10, 0L0, 5");

    var path = svg.append("svg:g").selectAll("path")
        .data(force.links())
        .enter().append("svg:path")
        .attr("class", "link")
        .attr("marker-end", "url(#end-arrow)");

    var circle = svg.append("svg:g").selectAll("circle")
        .data(force.nodes())
        .enter().append("svg:circle")
        .attr("r", function(d) {
            return 6 + Math.sqrt(d.ref);
        })
    .on("click", function(d) { updateInfo(d); })
        .call(force.drag);

    var text = svg.append("svg:g").selectAll("g")
        .data(force.nodes())
        .enter().append("svg:g");

    text.append("svg:text")
        .attr("x", 8)
        .attr("y",".31em")
        .attr("class", "shadow")
        .text(function(d) {return d.name;});

    text.append("svg:text")
        .attr("x", 8)
        .attr("y", ".31em")
        .text(function(d) {return d.name;});

    function tick() {
        path.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.x,
            dr = Math.sqrt(dx * dx + dy*dy);
        return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
        });

        circle.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
        text.attr("transform", function(d) {
            return "translate("+d.x+","+d.y+")";
        });
    }
    function updateInfo(patData) {
        var n = "<br>"
            document.getElementById('Patent').innerHTML=(typeof(patData.name)!='undefined'&&patData.name!='') ? 'Pat.No: '+patData.name+n : '';

        document.getElementById('Firstname').innerHTML=(typeof(patData.Firstname)!='undefined'&&patData.Firstname!='')?'First Name: '+patData.Firstname+n : '';

        document.getElementById('Lastname').innerHTML=(typeof(patData.Lastname)!='undefined'&&patData.Lastname!='')?'Last Name: '+ patData.Lastname+n : '';

        document.getElementById('Street').innerHTML=(typeof(patData.Street)!='undefined'&&patData.Street!='')?'Street: '+patData.Street+n:'';

        document.getElementById('City').innerHTML=(typeof(patData.city)!='undefined'&&patData.City!='')?'City: '+ patData.City+n:'';

        document.getElementById('State').innerHTML=(typeof(patData.State)!='undefined'&&patData.State!='')?'State: '+patData.State+n:'';

        document.getElementById('Country').innerHTML=(typeof(patData.Country)!='undefined'&&patData.Country!='')?'Country: '+patData.Country+n:'';

        document.getElementById('Zipcode').innerHTML=(typeof(patData.Zipcode)!='undefined'&&patData.Zipcode!='')?'Zipcode: '+patData.Zipcode+n:'';

        document.getElementById('PClass').innerHTML=(typeof(patData.PClass)!='undefined'&&patData.PClass!='')?'Patent Class: '+patData.PClass+n:'';

        document.getElementById('GYear').innerHTML=(typeof(patData.GYear)!='undefined'&&patData.GYear!='')?'Grant Year: '+patData.GYear+n:'';

        if (patData.ref==0) {
            document.getElementById('refby').innerHTML='0 (if you chose a leaf node, it is not accurate)'
        } else {
            document.getElementById('refby').innerHTML = patData.ref;
        }
    }
})
