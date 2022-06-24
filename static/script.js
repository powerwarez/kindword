/* donutGraph javascript */
function donutGraph(selector, percentage){

    'use strict';

    var height, width, radius, data, color, svg, g, bgArc, visArc, pie, path, vis;

    height = 150;
    width = 150;
    radius = Math.min(width, height) / 2;

    svg = d3.select(selector)
        .append('svg')
        .attr('viewBox', '0 0 ' + width + ' ' + height)
        .attr('preserveAspectRatio', 'none');

    g = svg.append('g')
        .attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');
  
    g.append('text')
        .text(percentage + '%')
        .attr('alignment-baseline', 'Hanging')
        .attr('text-anchor', 'middle');
  
    bgArc = d3.svg.arc()
        .innerRadius(radius / 1.25)
        .outerRadius(radius)
        .startAngle(0) //converting from degs to radians
        .endAngle(degTOrad(perTOdeg(100))); //just radians

    visArc = d3.svg.arc()
        .innerRadius(radius / 1.25) //1.2
        .outerRadius(radius) //1.04
        .cornerRadius(20)
        .startAngle(0) //converting from degs to radians
        .endAngle(degTOrad(perTOdeg(percentage))); //just radians

    g.append("path")
        .attr("d", bgArc)
        .attr('class', 'background');

    g.append("path")
        .attr("d", visArc)
        .attr('class', 'visual');

    function perTOdeg(per) {
        'use strict';
        return 360 * per / 100;
    }

    function degTOrad(deg) {
        'use strict';
        return deg * (Math.PI / 180);
    }

}

