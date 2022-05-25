//[Dashboard Javascript]

//Project:	DashboardX Admin - Responsive Admin Template
//Primary use:   Used only for the main dashboard (index.html)


$(function () {

  'use strict';
	
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
	
	
	
	var newCust = [[0, 2], [1, 3], [2,6], [3, 5], [4, 7], [5, 8], [6, 10]];
  		var retCust = [[0, 1], [1, 2], [2,5], [3, 3], [4, 5], [5, 6], [6,9]];
		
		var plot = $.plot($('#flotArea1'),[
            {
              data: newCust,
              label: 'Page views',
              color: '#e4e7ea'
            },
            {
              data: retCust,
              label: ' Active duration',
              color: '#00acc1 '
            }],
            {
              series: {
                lines: {
                  show: true,
                  lineWidth: 0,
                  fill: 0.8
                },
                shadowSize: 0
              },
              points: {
                show: false,
              },
              legend: {
                noColumns: 1,
                position: 'nw',
				show: false,
              },
              grid: {
                hoverable: true,
                clickable: true,
                borderColor: '#ddd',
                borderWidth: 0,
                labelMargin: 5,
                backgroundColor: '#fff'
              },
              yaxis: {
                min: 0,
                max: 15,
                color: '#eee',
                font: {
                  size: 10,
                  color: '#999'
                }
              },
              xaxis: {
                color: '#eee',
                font: {
                  size: 10,
                  color: '#999'
                }
              }
            });
	
	
	var optionsLine = {
	  chart: {
		height: 408,
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
	
	
	
	
	
	
		$("span.pie").peity("pie", {
			fill: ['#00b0ff ', '#d7d7d7', '#ffffff']
		})
	
	
	
	
}); // End of use strict



  
             

