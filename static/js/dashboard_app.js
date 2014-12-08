StandaloneDashboard(function(db){

	var myFirebaseRef = new Firebase("https://appbackr-dashboard.firebaseio.com/");

	kpi = new KPIGroupComponent();
	kpi.setDimensions (12, 2);
	kpi.setCaption('Core Static Analysis metrics');

	kpi.addKPI('kpi_apk_analysed', {
		caption: 'APKs Analysed',
		value: 0
	});

	myFirebaseRef.child("techeval/completions").on("value", function(snapshot) {
		kpi.updateKPI('kpi_apk_analysed', {
			caption: 'APKs Analysed',
			value: snapshot.numChildren()
		});
	});

	kpi.addKPI('kpi_apk_queue', {
		caption: 'APKs in Queue',
		value: 0
	});

	window.setInterval(function(kpi){
		$.ajax({
			type: 'GET',
			context: this,
			url: 'https://sqs.us-east-1.amazonaws.com/146141078993/DeepAPKInspection?Action=GetQueueAttributes&AttributeName.1=ApproximateNumberOfMessages',
			success: this.updateAPKQueue
		});
	}, 5000);

	updateAPKQueue = function(xml) {
		var value = $(xml).find('GetQueueAttributesResult').find('Attribute').find('Value').first().text();
		kpi.updateKPI('kpi_apk_queue', {
			caption: 'APKs in Queue',
			value: value
		});
	};

	kpi.addKPI('kpi_analysis_nodes', {
		caption: 'Analysis Nodes',
		value: 0
	});

	myFirebaseRef.child("techeval/instances").on("value", function(snapshot) {
		kpi.updateKPI('kpi_analysis_nodes', {
			caption: 'Analysis Nodes',
			value: snapshot.numChildren()
		});
	});

	kpi.addKPI('kpi_interpreted_results', {
		caption: 'Product Ready',
		value: 0
	});

	db.addComponent(kpi);

	var table = new TableComponent ('test');
	table.setCaption ("Analysed APKs");
	table.setDimensions(6, 4);
	//table.setRowsPerPage(7);
	table.addColumn ('instance', "Instance");
	table.addColumn ('timestamp', "Timestamp");
	table.addColumn ('apk_id', "APK ID");
	db.addComponent(table);

	myFirebaseRef.child("techeval/completions").orderByChild("timestamp").limitToFirst(10).once('value', function(snapshot) {
		snapshot.forEach(function(childSnapshot){
			table.addRow({instance: childSnapshot.val().instance, timestamp: childSnapshot.val().timestamp, apk_id: childSnapshot.key()});
		});
	});

	myFirebaseRef.child("techeval/completions").on("child_added", function(snapshot){
		table.addRow({instance: snapshot.val().instance, timestamp: snapshot.val().timestamp, apk_id: snapshot.key()});
	});

	/*var instance1 = new KPITableComponent();
	instance1.setDimensions (6, 2);
	instance1.setCaption('i-691eaa87');
	instance1.addKPI('last_update', {
		caption: 'Last Update',
		value: 0
	});
	instance1.addKPI('startup_time', {
		caption: 'Startup Time',
		value: 0
	});
	instance1.addKPI('status', {
		caption: 'Status',
		value: 0
	});
	db.addComponent(instance1);

	myFirebaseRef.child("techeval/instances/i-691eaa87").on("value", function(snapshot){
		instance1.updateKPI('last_update', {value: snapshot.val().last_update});
		//instance1.updateKPI('startup_time', {value: snapshot.val()});
		instance1.updateKPI('status', {value: snapshot.val().status});
	});*/

	/*initializeInstanceMonitor = function(childSnapshot){
		instance_id = childSnapshot.key();
		console.log(instance_id);

		var kpi = new KPITableComponent();
		kpi.setDimensions (6, 2);
		kpi.setCaption(instance_id);
		kpi.addKPI('last_update', {
			caption: 'Last Update',
			value: 0
		});
		kpi.addKPI('startup_time', {
			caption: 'Startup Time',
			value: 0
		});
		kpi.addKPI('status', {
			caption: 'Status',
			value: 0
		});
		db.addComponent(kpi);
	};

	myFirebaseRef.child("techeval/instances").once("value", function(snapshot) {
		snapshot.forEach(initializeInstanceMonitor);
	});*/
});