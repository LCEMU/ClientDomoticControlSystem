<html>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<link rel="stylesheet" type="text/css" href="style.css">
	<head>
	    <title>Configuración Sistema Domótico - Datos a registrar</title>
	</head>
	<body>

	<?php
		$wifi = $_POST['nombre'];
		$pass = $_POST['password'];
		$codeVerify = $_POST['codeVerify'];

		$config = "[WIFI]\nNOMBRE=".$wifi."\nPASSWORD=".$pass."\n\n[SECURITY]\nVERIFY_CODE=".$codeVerify;
		$nombre_archivo = "WifiConnect.cfg";

		if(file_exists($nombre_archivo)){
			$mensaje = "El Archivo $nombre_archivo se ha modificado";
		}else{
			$mensaje = "El Archivo $nombre_archivo se ha creado";
		}

		if($archivo = fopen($nombre_archivo, "w")){
			fwrite($archivo, $config);
			fclose($archivo);
		}
	?>
	<div class="out">
		<div class="in">
			<form action="end.php" method="post">
				<h2>DATOS INTRODUCIDOS
				<p class="aviso">Compruebe si estos datos son correctos y a continuación pulse 'Finalizar'.
				Si observa algun dato incorrecto pulse 'Atrás'.</p></h2>
				<table>
					<tr>
						<th>Red wifi seleccionada:</th>
						<td><?php echo $wifi; ?></td>
					</tr>
					<tr>
						<th>Password:</th>
						<td id="password" type="password"><?php echo $pass;?>
						<button class="btn btn-primary" type="button" onclick="mostrarPassword()">Mostrar</button>
						</td>
					</tr>
					<tr>
						<th>Código de verificación:</th>
						<td><?php echo $codeVerify; ?></td>
					</tr>
				</table>
				<input type='submit' value='Finalizar'>
			</form>
			<form action="register.php" method="post">
				<input type='submit' value='Atrás'>
			</form>
		</div>
	</div>
	</body>
</html>
<script>
        function mostrarPassword(){
                var tipo = document.getElementById("password");
                if (tipo.type == "password"){
                        tipo.type = "text";
                }else{
                        tipo.type = "password";
                }
        }
</script>
