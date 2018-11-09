<html>
	<link rel="stylesheet" type="text/css" href="style.css">
	<head>
	    <title>Configuración Sistema Domótico - Inicio</title>
	</head>
	<body>
		<div class="out">
			<div class="in">
				<?php
					$nombre_archivo = "WifiConnect.cfg";

					if(file_exists($nombre_archivo)){
						?>
						<h2>¡ Hola de nuevo !</h2>
						<p>Usted ya tiene una red wifi configurada para este dispositivo, ¿Desea cambiarla?</p>
						<form action="register.php" method="post">
							<input type="submit" value="Si">
						</form>
						<form action="end.php" method="post">
							<input type="submit" value="No">
						</form>
						<?php
					}else{
						?>
						<h2>¡ Bienvenido !</h2>
						Para iniciar el sistema que esta instalando deberá seguir los siguientes pasos:<br>
						[1] Comprobar que tras su dispositivo se le ofrecen unas indicaciones como<br>
						las mostradas a continuacion:<br><br>
						<img src="/home/pi/Pictures/INFO_RPI.png"><br><br>
						donde:<br>
						URL: es la ruta que usted ha escrito en el navegador<br>
						para acceder a esta pagina.<br>
						ESSID: es el nombre del la red wifi que genera su dispositivo domótico<br>
						PASS: es la contraseña del la red wifi que genera su dispositivo domótico<br>
						Esta información debe recordarla pues no puede modificarse.<br>
						[2] Al pulsar 'Comenzar' se le mostrará un formulario que debera completar<br>
						para configurar en su dispositivo domótico la red wifi del lugar<br>
						donde usted quiera instalar nuestro sistema.<br>
						[3] Si usted desconecta el sistema y lo vuelve a conectar deberá acceder de<br>
						nuevo a esta URL donde se le ofrecerá la posibilidad de mantener la configuración<br>
						realizada anteriormente o modificarla.
						<form action="register.php" method="post">
							<input type="submit" value="Comenzar">
						</form>
						<?php
					}
				?>
			<div>
		</div>
	</body>
</html>
