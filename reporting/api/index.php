 <?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
return_headers();

// Get MySQL Connection Details
$creds = file_get_contents("/var/www/secure/mysql_credentials.txt");
$credsObject = json_decode($creds, true);

$database = $credsObject["database"];
$hostname = $credsObject["server"];
$username = $credsObject["username"];
$password = $credsObject["password"];

$sqlConn =  new mysqli($hostname, $username, $password, $database);

// Determine which end point we are calling...
if($_GET['action'] == "facilities") {
	get_facilities($sqlConn);
}

if($_GET['action'] == "summaryData") {
	$readingDate = $_GET['readingDate'];
	$selectedFacility = $_GET['selectedFacility'];
	$selectedDevice = $_GET['selectedDevice'];
	get_summary_data($sqlConn, $readingDate, $selectedFacility, $selectedDevice);
}

if($_GET['action'] == "availableDates") {
	get_recent_dates($sqlConn);
}

if($_GET['action'] == "readingsTrend") {
	get_readings_trend($sqlConn);
}

if($_GET['action'] == 'readingsDetail') {
	get_readings_detail($sqlConn);
}

function return_headers() { // Allow from any origin
    if (isset($_SERVER['HTTP_ORIGIN'])) {
        header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Max-Age: 86400');    // cache for 1 day
    }

    // Access-Control headers are received during OPTIONS requests
    if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {

        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
            header("Access-Control-Allow-Methods: GET, POST, OPTIONS");         

        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
            header("Access-Control-Allow-Headers:        {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");

        exit(0);
    }
}

function get_facilities($sqlConn)
	{
		if ($sqlConn->connect_errno) {
			printf("Connect failed: %s\n", $sqlConn->connect_error);
			exit();
		}
		
		$sql = "SELECT * FROM Facilities";

		if ($result = $sqlConn->query($sql)) {
			
			$data = array();

			while ( $row = $result->fetch_assoc() ){
				$data[] = $row;
			}
			
			echo json_encode($data, JSON_NUMERIC_CHECK);
		
			$result->close();
		}
	}

function get_summary_data($sqlConn, $readingDate, $selectedFacility, $selectedDevice)
{
		if ($sqlConn->connect_errno) {
			printf("Connect failed: %s\n", $sqlConn->connect_error);
			exit();
		}
		
		$sql = "SELECT d.deviceID,
					   d.facilityID,
					   f.facilityName,
					   d.deviceName,
					   d.assignedTo,
					   MAX(r.loadDate) AS lastReading,
					   MAX(0.08) AS percentStooping,
					   MAX(0.03) AS percentBending,
					   MAX(0.89) AS percentUpright
				FROM Devices d
					 INNER JOIN
					 SensorReadings r on r.deviceID = d.deviceID
					 INNER JOIN
					 Facilities f ON f.facilityID = d.facilityID 
				WHERE d.facilityID = $selectedFacility
				AND	  CAST(readingTime AS DATE) = '$readingDate'
				AND ('$selectedDevice' = '0' OR d.deviceID = '$selectedDevice')
				GROUP BY d.deviceID,
					   d.facilityID,
					   f.facilityName,
					   d.deviceName,
					   d.assignedTo";
		if ($result = $sqlConn->query($sql)) {
			
			$data = array();

			while ( $row = $result->fetch_assoc() ){
				$data[] = $row;
			}
			
			echo json_encode($data, JSON_NUMERIC_CHECK);
		
			$result->close();
		}
}
	
function get_recent_dates($sqlConn)
{
		if ($sqlConn->connect_errno) {
			printf("Connect failed: %s\n", $sqlConn->connect_error);
			exit();
		}
		
		$sql = "SELECT DISTINCT CAST(loadDate AS DATE) AS readingDate
				FROM SensorReadings
				ORDER BY 1
				LIMIT 10";

		if ($result = $sqlConn->query($sql)) {
			
			$data = array();

			while ( $row = $result->fetch_assoc() ){
				$data[] = $row;
			}
			
			echo json_encode($data, JSON_NUMERIC_CHECK);
		
			$result->close();
		}
}
	
function get_readings_detail($sqlConn)
{
    if ($sqlConn->connect_errno) {
			printf("Connect failed: %s\n", $sqlConn->connect_error);
			exit();
		}
		
		$sql = "SELECT 	d.deviceID,
						d.facilityID,
						f.facilityName,
						d.deviceName,
						d.assignedTo,
						readingTime, 
						metricTypeID, 
						positionID, 
						uomID, 
						actualYaw, 
						actualPitch, 
						actualRoll, 
						setPointYaw, 
						setPointPitch, 
						setPointRoll, 
						loadDate, 
						readingID
				FROM Devices d
					 INNER JOIN
					 SensorReadings r on r.deviceID = d.deviceID
					 INNER JOIN
					 Facilities f ON f.facilityID = d.facilityID
					 
				ORDER BY readingTime";

		if ($result = $sqlConn->query($sql)) {
			
			$data = array();

			while ( $row = $result->fetch_assoc() ){
				$data[] = $row;
			}
			
			echo json_encode($data, JSON_NUMERIC_CHECK);
		
			$result->close();
		}
}

function get_readings_trend($sqlConn)
{
    if ($sqlConn->connect_errno) {
			printf("Connect failed: %s\n", $sqlConn->connect_error);
			exit();
		}
		
		$sql = "SELECT readingTime, 
					   positionID, 
					   actualPitch
				FROM   SensorReadings r
				ORDER BY readingTime";

		if ($result = $sqlConn->query($sql)) {
			
			$data = array();

			while ( $row = $result->fetch_assoc() ){
				$data[] = $row;
			}
			
			echo json_encode($data, JSON_NUMERIC_CHECK);
		
			$result->close();
		}
}
?>