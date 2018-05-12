( function ( $ ) {
    "use strict";   

    //pie chart
    var ctx = document.getElementById( "pieChart" );
    ctx.height = 150;
    var myChart = new Chart( ctx, {
        type: 'pie',
        data: {
            datasets: [ {
                data: [ 45, 25, 20, 10 ],
                backgroundColor: [
                                    "#4dbd74",
                                    "#20a8d8",
                                    "#ffc107",
                                    "#f86c6b"
                                ],
                hoverBackgroundColor: [
                                    "#4dbd74",
                                    "#20a8d8",
                                    "#ffc107",
                                    "#f86c6b"
                                ]

                            } ],
            labels: [
                            "< 30",
                            "< 60",
                            "< 90",
                            "> 90"
                        ]
        },
        options: {
            responsive: true
        }
    } );

    //doughut chart
    var ctx = document.getElementById( "doughutChart" );
    ctx.height = 150;
    var myChart = new Chart( ctx, {
        type: 'doughnut',
        data: {
            datasets: [ {
                data: [ 45, 25, 20, 10 ],
                backgroundColor: [
                                    "#4dbd74",
                                    "#f86c6b",
                                    "#20a8d8"
                                ],
                hoverBackgroundColor: [
                                    "#4dbd74",
                                    "#f86c6b",
                                    "#20a8d8"
                                ]

                            } ],
            labels: [
                            "Running",
                            "Stopped",
                            "Deallocated"
                        ]
        },
        options: {
            responsive: true
        }
    } );
} )( jQuery );