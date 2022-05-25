//[Dashboard Javascript]

//Project:	DashboardX Admin - Responsive Admin Template
//Primary use:   Used only for the main dashboard (index.html)


$(function () {

  'use strict';
	
	var plot = $.plot('#flotChart', [{
          data: flotSampleData3,
          color: '#303f9f',
          lines: {
            fillColor: { colors: [{ opacity: 0 }, { opacity: 0.5 }]}
          }
        },{
          data: flotSampleData4,
          color: '#ee1044',
          lines: {
            fillColor: { colors: [{ opacity: 0 }, { opacity: 0.5 }]}
          }
        }], {
    			series: {
    				shadowSize: 1,
            lines: {
              show: true,
              lineWidth: 2,
              fill: true
            }
    			},
          grid: {
            borderWidth: 0,
            labelMargin: 8
          },
    			yaxis: {
            			show: true,
    					min: 0,
    					max: 100,
            			ticks: [[0,''],[20,'20K'],[40,'40K'],[60,'60K'],[80,'80K']],
            			tickColor: 'rgba(255, 255, 255, 0.10)',
						font: {
							color: '#666666'
						  }
    			},
    			xaxis: {
            			show: true,
            			color: 'rgba(255, 255, 255, 0.10)',
            			ticks: [[25,'OCT 21'],[75,'OCT 22'],[100,'OCT 23'],[125,'OCT 24']],
						font: {
							color: '#666666'
						  }
          }
        });
	
		
	
		var options = {
            chart: {
                height: 470,
                type: 'bar',
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%'	
                },
            },
            dataLabels: {
                enabled: false
            },
			colors: ["#389f99", '#1976D2'],
            stroke: {
                show: true,
                width: 2,
                colors: ['transparent']
            },
            series: [{
                name: 'New User',
                data: [76, 85, 101, 98, 87, 105, 91]
            }, {
                name: 'Old User',
                data: [35, 41, 36, 26, 45, 48, 52]
            }],
            xaxis: {
                categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Set', 'Sun'],
            },
            fill: {
                opacity: 1

            },
			  legend: {
				position: 'top',
				horizontalAlign: 'left'
			  },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return "$ " + val + " thousands"
                    }
                }
            }
        }

        var chart = new ApexCharts(
            document.querySelector("#userflow"),
            options
        );

        chart.render();
	
	
	
		window.Apex = {
		  stroke: {
			width: 3
		  },
		  markers: {
			size: 0
		  },
		  tooltip: {
			fixed: {
			  enabled: true,
			}
		  }
		};

		var randomizeArray = function (arg) {
		  var array = arg.slice();
		  var currentIndex = array.length,
			temporaryValue, randomIndex;

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
		var sparklineData = [8,10,12,15,19,22,25,21,20,17,16,12,8,9,12,16,18,22,19,21,26,28,26,24];

		var spark2 = {
		  chart: {
			type: 'area',
			height: 160,
			sparkline: {
			  enabled: true
			},
		  },
		  stroke: {		  
			show: true,
			width: 0.5,
			curve: 'smooth'
		  },
		  fill: {
			opacity: 1,
			gradient: {
			  enabled: false
			}
		  },
		  series: [{
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
		  subtitle: {
			offsetX: 0,
			style: {
			  fontSize: '14px',
			  cssClass: 'apexcharts-yaxis-title'
			}
		  }
		}


		var spark2 = new ApexCharts(document.querySelector("#spark2"), spark2);
		spark2.render();
	
	
	
	
		WeatherIcon.add('icon1'	, WeatherIcon.SLEET , {stroke:false , shadow:false , animated:true } );
	
	
	
}); // End of use strict


// easypie chart
	$(function() {
		'use strict'
		$('.easypie').easyPieChart({
			easing: 'easeOutBounce',
			onStep: function(from, to, percent) {
				$(this.el).find('.percent').text(Math.round(percent));
			}
		});
		var chart = window.chart = $('.easypie').data('easyPieChart');
		$('.js_update').on('click', function() {
			chart.update(Math.random()*200-100);
		});
	});// End of use strict

  
             

