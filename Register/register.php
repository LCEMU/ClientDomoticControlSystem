<html>
	<link rel="stylesheet" type="text/css" href="style.css">
	<head>
	    <title>Configuración Sistema Domótico - Registro</title>
	</head>
	<body>
		<div class="out">
			<div class="in">
				<h2>REGISTRO
				<p class="aviso">> Rellene el siguiente formulario para configurar su sistema: </p></h2>
				<form action="info.php" method="post">

					<h3>Nombre WiFi: <span class="error">*</span></h3>
					<input type='text' name='nombre' placeholder="Introduzca aqui el nombre de su red wifi">

					<h3>Password: <span class="error">*</span></h3>
					<input type='password' name='password' id="password"  placeholder="Introduzca aqui la password de su red wifi">
					<button class="btn btn-primary" type="button" id="button-reg" onclick="mostrarPassword()">Mostrar</button>

					<h3>Código de verificación: <span class="error">*</span></h3>
					<input type='text' name='codeVerify' placeholder="Introduzca aqui el código situado tras el dispositivo">

					<br><input type='submit' value='Hecho!'>
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
