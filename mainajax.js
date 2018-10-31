$.ajax({
  //url: baseurl + '/api/repair/break',
  url: '/api/state/car/atlocation',
  type: 'POST',
  contentType: "application/json",
  data:  JSON.stringify({
  	"singleRecord": "True",
  	"attributes":{	"zip2":0,
  					"zip3":0,
  					"zip4":0,
  					"zip5":1,
  					"hod":1,
  					"numchild":1,
  					"income":3,
  					"gender":0,
  					"wealth":4,
  					"hv":1470,
  					"lcmed":483,
  					"lcavg":547,
  					"ic15":4,
  					"numprom":94,
  					"ramntall":177,
  					"maxramnt":10,
  					"lastgift":8,
  					"totalmonths":30,
  					"timelag":3,
  					"avggift":7.08
  				}
  }),
  success: function(data){
    console.write(data);
    console.write(data.Donor);
    if('Donor' in data){
       //eventdata.Donor
    }
  },
  error: function() {
     console.log("Error occured");
  }
  //dataType: 'jsonp'
  //success: function(data) {
  //   console.log(data);
  //},
});
