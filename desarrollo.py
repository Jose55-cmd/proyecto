from django.db import models
from django.utils import timezone # pyright: ignore[reportUnusedImport]

# ==========================================
# 1. CATÁLOGOS (Tablas de referencia)
# ==========================================

class CatPaises(models.Model):
    id_pais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo_iso = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        db_table = 'cat_paises'

class CatEstados(models.Model):
    id_estado = models.AutoField(primary_key=True)
    id_pais = models.ForeignKey(CatPaises, on_delete=models.CASCADE, db_column='id_pais')
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'cat_estados'

class CatCiudades(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    id_estado = models.ForeignKey(CatEstados, on_delete=models.CASCADE, db_column='id_estado')
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'cat_ciudades'

class CatEstatusPoliza(models.Model):
    id_estatus = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cat_estatus_poliza'

class CatEstatusSiniestro(models.Model):
    id_estatus = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'cat_estatus_siniestro'

class CatMarcas(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'cat_marcas'

class CatModelos(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    id_marca = models.ForeignKey(CatMarcas, on_delete=models.CASCADE, db_column='id_marca')
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'cat_modelos'

class CatMetodosPago(models.Model):
    id_metodo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cat_metodos_pago'

class CatMonedas(models.Model):
    id_moneda = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=5, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cat_monedas'

# ==========================================
# 2. ACTORES (Clientes, Aseguradoras, etc.)
# ==========================================

class Clientes(models.Model):
    TIPO_CLIENTE_CHOICES = [
        ('NATURAL', 'Natural'),
        ('JURIDICA', 'Jurídica'),
        ('GUBERNAMENTAL', 'Gubernamental'),
    ]
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]

    id_cliente = models.AutoField(primary_key=True)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES)
    tipo_documento = models.CharField(max_length=3)
    numero_documento = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100, null=True, blank=True)
    telefono_movil = models.CharField(max_length=20, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100)
    direccion = models.TextField(null=True, blank=True)
    id_ciudad = models.ForeignKey(CatCiudades, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_ciudad')
    profesion_oficio = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'clientes'
        unique_together = (('tipo_documento', 'numero_documento'),)

class CompaniasSeguros(models.Model):
    id_compania = models.AutoField(primary_key=True)
    rif = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20, null=True, blank=True)
    persona_contacto = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'companias_seguros'

class Intermediarios(models.Model):
    id_intermediario = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=150)
    codigo_sudeaseg = models.CharField(max_length=50, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'intermediarios'

class Financiadoras(models.Model):
    id_financiadora = models.AutoField(primary_key=True)
    rif = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'financiadoras'

# ==========================================
# 3. CORE DEL NEGOCIO (Ramos, Pólizas, Recibos)
# ==========================================

class Ramos(models.Model):
    id_ramo = models.AutoField(primary_key=True)
    nombre_ramo = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'ramos'

class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_ramo = models.ForeignKey(Ramos, on_delete=models.CASCADE, db_column='id_ramo')
    nombre_producto = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'productos'

class Vehiculos(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, db_column='id_cliente')
    id_modelo = models.ForeignKey(CatModelos, on_delete=models.CASCADE, db_column='id_modelo')
    anio = models.IntegerField()
    placa = models.CharField(max_length=20, unique=True)
    serial_motor = models.CharField(max_length=50)
    serial_carroceria = models.CharField(max_length=50)
    color = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'vehiculos'

class Polizas(models.Model):
    id_poliza = models.AutoField(primary_key=True)
    numero_poliza = models.CharField(max_length=50)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, db_column='id_cliente')
    id_vehiculo = models.ForeignKey(Vehiculos, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_vehiculo')
    id_compania = models.ForeignKey(CompaniasSeguros, on_delete=models.CASCADE, db_column='id_compania')
    id_ramo = models.ForeignKey(Ramos, on_delete=models.CASCADE, db_column='id_ramo')
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE, db_column='id_producto')
    id_estatus = models.ForeignKey(CatEstatusPoliza, on_delete=models.CASCADE, default= 1, db_column='id_estatus') # pyright: ignore[reportArgumentType]
    id_moneda = models.ForeignKey(CatMonedas, on_delete=models.CASCADE, db_column='id_moneda')
    suma_asegurada = models.DecimalField(max_digits=15, decimal_places=2)
    prima_neta = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_emision = models.DateField()
    fecha_fin = models.DateField()
    vigencia_desde = models.DateField()
    vigencia_hasta = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'polizas'

class RecibosPrimas(models.Model):
    ESTATUS_COBRO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
        ('Anulado', 'Anulado'),
    ]
    id_recibo = models.AutoField(primary_key=True)
    id_poliza = models.ForeignKey(Polizas, on_delete=models.CASCADE, db_column='id_poliza')
    monto_cuota = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_vencimiento = models.DateField()
    estatus_cobro = models.CharField(max_length=20, choices=ESTATUS_COBRO_CHOICES, default='Pendiente')

    class Meta:
        db_table = 'recibos_primas'

class Siniestros(models.Model):
    id_siniestro = models.AutoField(primary_key=True)
    numero_siniestro = models.CharField(max_length=50)
    id_poliza = models.ForeignKey(Polizas, on_delete=models.CASCADE, db_column='id_poliza')
    id_estatus = models.ForeignKey(CatEstatusSiniestro, on_delete=models.CASCADE, db_column='id_estatus')
    fecha_ocurrencia = models.DateTimeField()
    fecha_notificacion = models.DateTimeField(auto_now_add=True)
    descripcion_evento = models.TextField()
    lugar_evento = models.CharField(max_length=200, null=True, blank=True)
    monto_estimado = models.DecimalField(max_digits=15, decimal_places=2, default=0.00) # pyright: ignore[reportUnknownVariableType, reportArgumentType]
    monto_aprobado = models.DecimalField(max_digits=15, decimal_places=2, default=0.00) # pyright: ignore[reportUnknownVariableType, reportArgumentType]
    nombre_contacto_emergencia = models.CharField(max_length=100, null=True, blank=True)
    telefono_contacto_emergencia = models.CharField(max_length=20, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'siniestros'

# ==========================================
# 4. SEGURIDAD Y USUARIOS
# ==========================================

class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'roles'

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE, db_column='id_rol')
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    nombre_completo = models.CharField(max_length=100)
    ultimo_login = models.DateTimeField(null=True, blank=True)
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'usuarios'
