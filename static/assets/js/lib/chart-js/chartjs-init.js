jQuery(document).ready(function(){
    var running_vm=10;
    var stopped_vm=10;
    var total_vms=10;
    var storage_count;
   jQuery.ajax({
       method: "GET",
       url: "/vms",
     success: function( vms ) {
	running_vm = vms.vm_running;
        stopped_vm = vms.vm_stopped;
        total_vms = running_vm + stopped_vm;
      jQuery('#vm_running').text(running_vm);
      jQuery('#vm_stopped').text(stopped_vm);
      jQuery('#vm_total').text(total_vms);
      //doughut chart
    var ctx = document.getElementById( "doughutChart" );
    ctx.height = 150;
    var myChart = new Chart( ctx, {
        type: 'doughnut',
        data: {
            datasets: [ {
                data: [ running_vm, stopped_vm, total_vms,10 ],
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
    });
    }
   });
   jQuery.ajax({
       method: "GET",
       url: "/storage",
     success: function( storage ) {
        storage_count = storage.number;
      jQuery('#blob').text(storage_count);
    }
 });

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



});
	


