//[Dashboard Javascript]

//Project:	DashboardX Admin - Responsive Admin Template
//Primary use:   Used only for the main dashboard (index.html)


$(function () {

  'use strict';
	
	Apex.grid = {
	  padding: {
		right: 0,
		left: 0
	  }
	}

	Apex.dataLabels = {
	  enabled: false
	}

	var randomizeArray = function (arg) {
	  var array = arg.slice();
	  var currentIndex = array.length, temporaryValue, randomIndex;

	  while (0 !== currentIndex) {

		randomIndex = Math.floor(Math.random() * currentIndex);
		currentIndex -= 1;

		temporaryValue = array[currentIndex];
		array[currentIndex] = array[randomIndex];
		array[randomIndex] = temporaryValue;
	  }

	  return array;
	}

	// data for the sparklines that appear below header area
	var sparklineData = [47, 45, 54, 38, 56, 24, 65, 31, 37, 39, 62, 51, 35, 41, 35, 27, 93, 53, 61, 27, 54, 43, 19, 46];

	var spark1 = {
	  chart: {
		id: 'sparkline1',
		group: 'sparklines',
		type: 'area',
		height: 308,
		sparkline: {
		  enabled: true
		},
	  },
	  stroke: {
		curve: 'straight'
	  },
	  fill: {
		opacity: 1,
		colors: ['#303f9f']
	  },
	  series: [{
		name: 'Sales',
		data: randomizeArray(sparklineData)
	  }],
	  labels: [...Array(24).keys()].map(n => `2018-09-0${n+1}`),
	  yaxis: {
		min: 0
	  },
	  xaxis: {
		type: 'datetime',
	  },
	  colors: ['#303f9f'],
	  
	}
	
	new ApexCharts(document.querySelector("#spark1"), spark1).render();
	
	
	
	
	
	  $("#barchart4").sparkline([32,24,26,24,32,26,40,34,22,24], {
			type: 'bar',
			height: '50',
			width: '80%',
			barWidth: 5,
			barSpacing: 4,
			barColor: '#ee1044',
		});
	
	
	
	var options = {
      chart: {
        height: 285,
        type: 'line',
      },
      colors: ['#303f9f', '#ee1044'],
      series: [{
        name: 'Daly Earnings',
        type: 'column',
        data: [440, 505, 414, 671, 227, 413, 201, 352, 752, 320, 257, 160]
      }, {
        name: 'Overview',
        type: 'line',
        data: [23, 42, 35, 27, 43, 22, 17, 31, 22, 22, 12, 16]
      }],
      stroke: {
        width: [0, 4]
      },
      // labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      labels: ['01 Jan 2001', '02 Jan 2001', '03 Jan 2001', '04 Jan 2001', '05 Jan 2001', '06 Jan 2001', '07 Jan 2001', '08 Jan 2001', '09 Jan 2001', '10 Jan 2001', '11 Jan 2001', '12 Jan 2001'],
      xaxis: {
        type: 'datetime'
      },
      yaxis: [{
        title: {
          text: 'Daly Earnings',
        },

      }, {
        opposite: true,
        title: {
          text: 'Overview'
        }
      }]

    }

    var chart = new ApexCharts(
      document.querySelector("#chart-lca"),
      options
    );

    chart.render();
	
	
	
	
	
	var customerData = {
		labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov" ],
		datasets: [{
			label: 'New Tickets',
			data: [21, 34, 44, 34, 26, 22, 19, 15],
			backgroundColor: [
				'#e4e4e4', '#e4e4e4', '#e4e4e4', '#e4e4e4', '#ee1044', '#e4e4e4', '#e4e4e4', '#e4e4e4',
			],
			borderColor: [
				'#e4e4e4', '#e4e4e4', '#e4e4e4', '#e4e4e4', '#ee1044', '#e4e4e4', '#e4e4e4', '#e4e4e4',
			],
			borderWidth: 1,
			fill: false
		}
		]
	};
	var customerOptions = {
		scales: {
			xAxes: [{
			barPercentage: 1,
			position: 'bottom',
			display: true,
			gridLines: {
				display: false,
				drawBorder: false,
			},
			ticks: {
				display: false, //this will remove only the label
				stepSize: 300,
			}
			}],
			yAxes: [{
				display: false,
				gridLines: {
					drawBorder: false,
					display: true,
					color: "#f0f3f6",
					borderDash: [8, 4],
				},
				ticks: {
					display: false,
					beginAtZero: true,
				},
			}]
		},
		legend: {
			display: false
		},
		tooltips: {
			enabled: false,
			backgroundColor: 'rgba(0, 0, 0, 1)',
		},
		plugins: {
			datalabels: {
				display: false,
				align: 'center',
				anchor: 'center'
			}
		}				
	};
	if ($("#customer").length) {
		var barChartCanvas = $("#customer").get(0).getContext("2d");
		// This will get the first returned node in the jQuery collection.
		if(screen.width>767) {
			var chartHeight = document.getElementById("customer");
			chartHeight.height = 60;
		}
		var barChart = new Chart(barChartCanvas, {
			type: 'bar',
			data: customerData,
			options: customerOptions
		});
	}
	
	
	
	
	
	var ordersData = {
			labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov" ],
			datasets: [{
				label: 'New Tickets',
				data: [19, 18, 17, 14, 43, 24, 18, 17],
				backgroundColor: [
					'#e4e4e4', '#e4e4e4', '#e4e4e4', '#e4e4e4', '#1976D2', '#e4e4e4', '#e4e4e4', '#e4e4e4',
				],
				borderColor: [
					'#e4e4e4', '#e4e4e4', '#e4e4e4', '#e4e4e4', '#1976D2', '#e4e4e4', '#e4e4e4', '#e4e4e4',
				],
				borderWidth: 1,
				fill: false
			}
			]
		};
		var ordersOptions = {
			scales: {
				xAxes: [{
				barPercentage: 1,
				position: 'bottom',
				display: true,
				gridLines: {
					display: false,
					drawBorder: false,
				},
				ticks: {
					display: false, //this will remove only the label
					stepSize: 300,
				}
				}],
				yAxes: [{
					display: false,
					gridLines: {
						drawBorder: false,
						display: true,
						color: "#f0f3f6",
						borderDash: [8, 4],
					},
					ticks: {
						display: false,
						beginAtZero: true,
					},
				}]
			},
			legend: {
				display: false
			},
			tooltips: {
				enabled: false,
				backgroundColor: 'rgba(0, 0, 0, 1)',
			},
			plugins: {
				datalabels: {
					display: false,
					align: 'center',
					anchor: 'center'
				}
			}				
		};
		if ($("#orders").length) {
			var barChartCanvas = $("#orders").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			if(screen.width>767) {
				var chartHeight = document.getElementById("orders");
				chartHeight.height = 60;
			}
			var barChart = new Chart(barChartCanvas, {
				type: 'bar',
				data: ordersData,
				options: ordersOptions
			});
		}
		var growthData = {
			labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov" ],
			datasets: [{
				label: 'New Tickets',
				data: [13, 18, 31, 38, 48, 34, 25, 20],
				backgroundColor: [
					'#e4e4e4', '#e4e4e4', '#e4e4e4', '#e4e4e4', '#303f9f', '#e4e4e4', '#e4e4e4', '#e4e4e4',
				],
				borderColor: [
					'#e4e4e4', '#e4e4e4', '#e4e4e4', '#e4e4e4', '#303f9f', '#e4e4e4', '#e4e4e4', '#e4e4e4',
				],
				borderWidth: 1,
				fill: false
			}
			]
		};
		var growthOptions = {
			scales: {
				xAxes: [{
				barPercentage: 1,
				position: 'bottom',
				display: true,
				gridLines: {
					display: false,
					drawBorder: false,
				},
				ticks: {
					display: false, //this will remove only the label
					stepSize: 300,
				}
				}],
				yAxes: [{
					display: false,
					gridLines: {
						drawBorder: false,
						display: true,
						color: "#f0f3f6",
						borderDash: [8, 4],
					},
					ticks: {
						display: false,
						beginAtZero: true,
					},
				}]
			},
			legend: {
				display: false
			},
			tooltips: {
				enabled: false,
				backgroundColor: 'rgba(0, 0, 0, 1)',
			},
			plugins: {
				datalabels: {
					display: false,
					align: 'center',
					anchor: 'center'
				}
			}				
		};
		if ($("#growth").length) {
			var barChartCanvas = $("#growth").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			if(screen.width>767) {
				var chartHeight = document.getElementById("growth");
				chartHeight.height = 60;
			}
			var barChart = new Chart(barChartCanvas, {
				type: 'bar',
				data: growthData,
				options: growthOptions
			});
		}
		var revenueData = {
			labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov" ],
			datasets: [{
				label: 'New Tickets',
				data: [13, 18, 31, 38, 33, 24, 19, 13],
				backgroundColor: [
					'#e4e4e4', '#e4e4e4', '#e4e4e4', '#e4e4e4', '#ff8f00', '#e4e4e4', '#e4e4e4', '#e4e4e4',
				],
				borderColor: [
					'#e4e4e4', '#e4e4e4', '#e4e4e4', '#e4e4e4', '#ff8f00', '#e4e4e4', '#e4e4e4', '#e4e4e4',
				],
				borderWidth: 1,
				fill: false
			}
			]
		};
		var revenueOptions = {
			scales: {
				xAxes: [{
				barPercentage: 1,
				position: 'bottom',
				display: true,
				gridLines: {
					display: false,
					drawBorder: false,
				},
				ticks: {
					display: false, //this will remove only the label
					stepSize: 300,
				}
				}],
				yAxes: [{
					display: false,
					gridLines: {
						drawBorder: false,
						display: true,
						color: "#f0f3f6",
						borderDash: [8, 4],
					},
					ticks: {
						display: false,
						beginAtZero: true,
					},
				}]
			},
			legend: {
				display: false
			},
			tooltips: {
				enabled: false,
				backgroundColor: 'rgba(0, 0, 0, 1)',
			},
			plugins: {
				datalabels: {
					display: false,
					align: 'center',
					anchor: 'center'
				}
			}				
		};
		if ($("#revenue").length) {
			var barChartCanvas = $("#revenue").get(0).getContext("2d");
			// This will get the first returned node in the jQuery collection.
			if(screen.width>767) {
				var chartHeight = document.getElementById("revenue");
				chartHeight.height = 60;
			}
			var barChart = new Chart(barChartCanvas, {
				type: 'bar',
				data: revenueData,
				options: revenueOptions
			});
		}
	
	
	
	
	
	
	
	
}); // End of use strict



  
             

