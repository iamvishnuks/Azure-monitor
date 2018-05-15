jQuery(document).ready(function(){
    var running_vm=10;
    var stopped_vm=10;
    var total_vms=10;
    var storage_count;
    var less_ninenty;
    var less_sixty;
    var less_thirty;
    var greater_ninety;
   jQuery.ajax({
       method: "GET",
       url: "/vms",
     success: function( vms ) {
	running_vm = vms.vm_running;
        stopped_vm = vms.vm_stopped;
        deallocated_vm = vms.vm_deallocated;
        total_vms = running_vm + stopped_vm;
      jQuery('#vm_running').text(running_vm);
      jQuery('#vm_stopped').text(stopped_vm);
      jQuery('#vm_total').text(total_vms);
      jQuery('#vm_deallocated').text(deallocated_vm);
      //doughut chart
    var ctx = document.getElementById( "doughutChart" );
    ctx.height = 150;
    var myChart = new Chart( ctx, {
        type: 'doughnut',
        data: {
            datasets: [ {
                data: [ running_vm, stopped_vm, deallocated_vm ],
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
 jQuery.ajax({
       method: "GET",
       url: "/resources",
     success: function( resources ) {
        less_thirty = resources.age.less_thirty;
        less_sixty = resources.age.less_sixty;
        less_ninenty = resources.age.less_ninety;
        greater_ninenty = resources.age.greater_ninety;
      console.log(resources);
      jQuery('#less_thirty').text(less_thirty);
      jQuery('#less_sixty').text(less_sixty);
      jQuery('#less_ninenty').text(less_ninenty);
      jQuery('#greater_ninenty').text(greater_ninenty);
     //pie chart
    var ctx = document.getElementById( "pieChart" );
    ctx.height = 150;
    var myChart = new Chart( ctx, {
        type: 'pie',
        data: {
            datasets: [ {
                data: [ less_thirty, less_sixty, less_ninenty, greater_ninenty ],
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
    });
    }
 });
});

   
