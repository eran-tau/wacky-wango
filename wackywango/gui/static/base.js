function first_letter_to_upper(str){
    return str.charAt(0).toUpperCase() + str.slice(1)
}

function load_users(){
    $.ajax({url: api_url+"/users", success: function(result){

        jQuery.each(result.result, function(id, name) {
            $("#base-table").append("<tr onclick=\"window.location='"+id+"';\"><td>"+id+"</td><td>"+name+"</td></a></tr>");
            });

    }});

};

function load_user(user_id){
    $.ajax({url: api_url+"/users/"+user_id, success: function(result){
        jQuery.each(result.result, function(id, name) {
            $("#base-table").append("<tr><td>"+first_letter_to_upper(id)+"</td><td>"+name+"</td></a></tr>");
            });
    }});
};

function snapshot_image_container(snapshot_id,img_url){
    return `<div class="col-lg-3 col-md-4 col-6">
      <a href="`+snapshot_id+`" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail" src="`+img_url+`" alt="">
          </a>
    </div>`;
}

function pose_container(data){
    return `
      <div class="table-responsive">
        <table class="table table-striped table-sm table-hover">
          <thead>
            <tr>
              <th>Data</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Rotation X</td><td>`+data.rotation.x+`</td></a></tr>
            <tr><td>Rotation Y</td><td>`+data.rotation.y+`</td></a></tr>
            <tr><td>Rotation Z</td><td>`+data.rotation.z+`</td></a></tr>
            <tr><td>Rotation W</td><td>`+data.rotation.w+`</td></a></tr>
            <tr><td>Translation X</td><td>`+data.translation.x+`</td></a></tr>
            <tr><td>Translation Y</td><td>`+data.translation.y+`</td></a></tr>
            <tr><td>Translation Z</td><td>`+data.translation.z+`</td></a></tr>

          </tbody>
        </table>
      </div>
`;
}

function feelings_container(data){
    res = `
      <div class="table-responsive">
        <table class="table table-striped table-sm table-hover">
          <thead>
            <tr>
              <th>Data</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>`;
    jQuery.each(data, function(name, value) {
        res += `<tr><td>`+name+`</td><td>`+value+`</td></a></tr>`;
    });

    res += `
          </tbody>
        </table>
      </div>
    `;
    return res;
}



function load_snapshots(user_id){
    $.ajax({url: api_url+"/users/"+user_id+"/snapshots", success: function(result){
        jQuery.each(result.result, function(id, results) {
            $.ajax({url: api_url+"/users/"+user_id+"/snapshots/"+results.id+"/color_image/", success: function(image_data){
                $("#snapshot-album").append(snapshot_image_container(results.id,image_data.result));
            }});
        });
    }});
}


function load_snapshot(user_id,snapshot_id){
    $.ajax({url: api_url+"/users/"+user_id+"/snapshots/"+snapshot_id, success: function(result){
        var myDate = new Date(parseInt(result.result.snapshot_timestamp));
        $("#snapshot-details").append('<div>'+myDate.toGMTString()+'</div>');
        jQuery.each(result.result.snapshot_types, function(id, parser_type) {
            $.ajax({url: api_url+"/users/"+user_id+"/snapshots/"+snapshot_id+"/"+parser_type.parser_type+"/", success: function(parser_data){
                if ((parser_type.parser_type == "color_image") || (parser_type.parser_type == "depth_image")) {
                    $("#snapshot-details").append('<img src="'+parser_data.result+'"/>');
                }
                if (parser_type.parser_type == "pose"){
                    $("#snapshot-details").append(pose_container(parser_data.result));
                }
                if (parser_type.parser_type == "feelings"){
                    $("#snapshot-details").append(feelings_container(parser_data.result));
                }
//                $("#snapshot-album").append(snapshot_image_container(results.id,image_data.result));
            }});
        });
    }});
}


function load_feelings_chart(user_id){
    data = {};

    labels = [];
    exhaustion_graph = [];
    happiness_graph = [];
    hunger_graph = [];
    thirst_graph = [];

    //I couldnt make $.when work to resolve the promises. I ended with a lame implementation...
    counter_obj = {"cnt":0,"total":-1}

    $.ajax({url: api_url+"/users/"+user_id+"/snapshots", success: function(result){
        counter_obj['total'] = result.result.length-1;
        jQuery.each(result.result, function(id, results) {
            $.ajax({url: api_url+"/users/"+user_id+"/snapshots/"+results.id+"/feelings/", success: function(feelings_data){
                        counter_obj['cnt']++;
                        labels.push(results.snapshot_timestamp);
                        exhaustion_graph.push({x:results.snapshot_timestamp,y:feelings_data.result.exhaustion});
                        happiness_graph.push({x:results.snapshot_timestamp,y:feelings_data.result.happiness});
                        hunger_graph.push({x:results.snapshot_timestamp,y:feelings_data.result.hunger});
                        thirst_graph.push({x:results.snapshot_timestamp,y:feelings_data.result.thirst});
                }});
        });
    }})
    create_chart_when_ready(labels,exhaustion_graph,happiness_graph,hunger_graph,thirst_graph,counter_obj);
}

function create_chart_when_ready(labels,exhaustion_graph,happiness_graph,hunger_graph,thirst_graph,counter_obj){
    if (counter_obj['cnt']==counter_obj['total']){
        create_chart(labels,exhaustion_graph,happiness_graph,hunger_graph,thirst_graph);
    } else {
        window.setTimeout(() => {
            create_chart_when_ready(labels,exhaustion_graph,happiness_graph,hunger_graph,thirst_graph,counter_obj);
        }, 1000);
    }

}

async function create_chart(labels,exhaustion_graph,happiness_graph,hunger_graph,thirst_graph){
  // Graphs
  labels = labels.sort();

  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        data: exhaustion_graph,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff',
        label: 'Exhaustion'
      },
      {
        data: happiness_graph,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#ff0000',
        borderWidth: 4,
        pointBackgroundColor: '#ff0000',
        label: 'Happiness'
      },
      {
        data: hunger_graph,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#00ff00',
        borderWidth: 4,
        pointBackgroundColor: '#00ff00',
        label: 'Hunger'
      },
      {
        data: thirst_graph,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#0000ff',
        borderWidth: 4,
        pointBackgroundColor: '#0000ff',
        label: 'Thirst'
      }
      ]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: true
      }
    }
  })


}