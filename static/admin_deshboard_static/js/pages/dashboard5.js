//[Dashboard Javascript]

//Project:	DashboardX Admin - Responsive Admin Template
//Primary use:   Used only for the main dashboard (index.html)


$(function () {

  'use strict';
	
	$("span.pie").peity("pie", {
        fill: ['#1976D2', '#f7f7f7', '#ffffff']
    })
	
	// Donut Charts

	$('.donut').peity('donut')
	
	$(".bar").peity("bar", {
        fill: ["#1976D2", "#f7f7f7"],
		height: 60,
		width: 100,
    })
	

    $(".line").peity("line",{
        fill: '#1976D2',
        stroke:'#1976D2',
		height: 60,
		width: 100,
    })
	
	/*********** REAL TIME UPDATES **************/

    var data = [], totalPoints = 550;

    function getRandomData() {
      if (data.length > 0)
      data = data.slice(1);
      while (data.length < totalPoints) {
        var prev = data.length > 0 ? data[data.length - 1] : 50,
        y = prev + Math.random() * 10 - 5;
        if (y < 0) {
          y = 0;
        } else if (y > 100) {
          y = 100;
        }
        data.push(y);
      }
      var res = [];
      for (var i = 0; i < data.length; ++i) {
        res.push([i, data[i]])
      }
      return res;
    }


    // Set up the control widget
	 var updateInterval = 30;

   var plot4 = $.plot('#flotRealtime1', [ getRandomData() ], {
      colors: ['#1976D2'],
		  series: {
        lines: {
          show: true,
          lineWidth: 1,
			fill: 0.9,
        },
        shadowSize: 0	// Drawing is faster without shadows
		  },
      grid: {
        borderColor: '#ddd',
        borderWidth: 1,
        labelMargin: 5
		  },
      xaxis: {
        color: '#eee',
        font: {
          size: 10,
          color: '#999'
        }
      },
		  yaxis: {
				min: 0,
				max: 100,
        color: '#eee',
        font: {
          size: 10,
          color: '#999'
        }
		  }
	 });


	 function update_plot4() {
		  plot4.setData([getRandomData()]);
		  plot4.draw();
		  setTimeout(update_plot4, updateInterval);
	 }

	 update_plot4();
	
	
	
	// ------------------------------
        // pole chart
        // ------------------------------
        // based on prepared DOM, initialize echarts instance
            var poleChart = echarts.init(document.getElementById('pole-chart'));
            // Data style
            var dataStyle = {
                normal: {
                    label: {show: false},
                    labelLine: {show: false}
                }
            };

            // Placeholder style
            var placeHolderStyle = {
                normal: {
                    color: 'rgba(0,0,0,0)',
                    label: {show: false},
                    labelLine: {show: false}
                },
                emphasis: {
                    color: 'rgba(0,0,0,0)'
                }
            };
            var option = {
                title: {
                    text: 'Search Data',
                    subtext: 'Weekly Data',
                    x: 'center',
                    y: 'center',
                    itemGap: 10,
                    textStyle: {
                        color: 'rgba(30,144,255,0.8)',
                        fontSize: 19,
                        fontWeight: '500'
                    }
                },

                // Add tooltip
                tooltip: {
                    show: true,
                    formatter: "{a} <br/>{b}: {c} ({d}%)"
                },

                // Add legend
                legend: {
                    orient: 'vertical',
                    x: document.getElementById('pole-chart').offsetWidth / 2,
                    y: 30,
                    x: '55%',
                    itemGap: 15,
                    data: ['Net','Direct','Email']
                },

                // Add custom colors
                color: ['#689f38', '#38649f', '#ff8f00'],
 
                // Add series
                series: [
                    {
                        name: '1',
                        type: 'pie',
                        clockWise: false,
                        radius: ['75%', '90%'],
                        itemStyle: dataStyle,
                        data: [
                            {
                                value: 60,
                                name: 'Monday'
                            },
                            {
                                value: 40,
                                name: 'invisible',
                                itemStyle: placeHolderStyle
                            }
                        ]
                    },

                    {
                        name: '2',
                        type:'pie',
                        clockWise: false,
                        radius: ['60%', '75%'],
                        itemStyle: dataStyle,
                        data: [
                            {
                                value: 30, 
                                name: 'Tuesday'
                            },
                            {
                                value: 70,
                                name: 'invisible',
                                itemStyle: placeHolderStyle
                            }
                        ]
                    },

                    {
                        name: '3',
                        type: 'pie',
                        clockWise: false,
                        radius: ['45%', '60%'],
                        itemStyle: dataStyle,
                        data: [
                            {
                                value: 10, 
                                name: 'Wednesday'
                            },
                            {
                                value: 90,
                                name: 'invisible',
                                itemStyle: placeHolderStyle
                            }
                        ]
                    }
                ]
            };
        poleChart.setOption(option);
	
	
	var optionsLine = {
	  chart: {
		height: 463,
		type: 'line',
		zoom: {
		  enabled: false
		},
	  },
	  stroke: {
		curve: 'smooth',
		width: 2
	  },
	  colors: ["#303f9f", '#1976D2'],
	  series: [{
		  name: "Live Resource",
		  data: [1, 15, 26, 20, 33, 27]
		},
		{
		  name: "Feature Resource",
		  data: [3, 33, 21, 42, 19, 32]
		}
	  ],
	  markers: {
		size: 6,
		strokeWidth: 0,
		hover: {
		  size: 9
		}
	  },
	  grid: {
		show: true
	  },
	  labels: ['01/15/2019', '01/16/2019', '01/17/2019', '01/18/2019', '01/19/2019', '01/20/2019'],
	  xaxis: {
		tooltip: {
		  enabled: false
		}
	  },
	  legend: {
		position: 'top',
		horizontalAlign: 'right',
		offsetY: -20
	  }
	}

	var chartLine = new ApexCharts(document.querySelector('#line-adwords'), optionsLine);
	chartLine.render();
	
	
	
	
		
	
	
	
	
	
	
}); // End of use strict



  
             

