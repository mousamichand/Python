<h3>VMware Cloud Usage Script</h3>
Overview
This script retrieves all VMware clouds available in Morpheus, fetches all hosts within each cloud, and calculates resource usage statistics. The results are then presented in a tabular format.

<h4>Features </h4>
<ul>
<li>Fetches all VMware clouds from Morpheus</li>

<li>Retrieves all hosts within each cloud</li>

<li>Calculates usage statistics for: </li>

<ul>
<li>Storage Usage</li>
<li>CPU Usage</li>
<li>Memory Usage</li>
</ul>

<li>Presents data in a tabular format for easy analysis </li>

<li>Triggers email notifications if resource usage exceeds predefined thresholds</li>
</ul>


<h4>Configuration</h4>
<ul><li>Create Cypher entry in  Morpheus for vcenter user and password.Line 14 and 16. </li>
<li>Configure email settings for notifications. Line 58 -63 </li>
</ul>

<h4>Output</h4>
<ul><li>The script generates a tabular report showing cloud- and host-level statistics </li>
<li>Email Notification is sent if resource usage exceeds predefined thresholds </li>
</ul>
