import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Image, TouchableOpacity, StyleSheet, Alert, ScrollView } from 'react-native';
import * as Location from 'expo-location';
import * as SecureStore from 'expo-secure-store';
import { springApi } from '../config/api';

export default function ConfirmScreen({ route, navigation }) {

  // Recuperar parámetros de la navegación (parametros enviados desde CameraScreen)
  const { matriculaDetectada, fotoUri } = route.params;  
  const [matricula, setMatricula] = useState(matriculaDetectada);
  const [location, setLocation] = useState(null);
  const [loading, setLoading] = useState(false);

   
  // Pedimos permiso de ubicacion al usuarios y obtener coordenadas para la incidencia
 useEffect(() => {

    setLocation({
      latitude: 24.788438, 
      longitude: -107.399612,
    });

    
    /*(async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permiso denegado', 'Necesitamos tu ubicación para registrar la incidencia.');
        return;
      }

      let loc = await Location.getCurrentPositionAsync({});
      setLocation(loc.coords);
    })();*/
  }, []);

  // Funcion asincrona para confirmar y enviar la incidencia a la API de Java
  const confirmarIncidencia = async () => {
    // Mensajes de validacion para usuario
    if (!location) {
      Alert.alert("Esperando GPS...", "Por favor espera a que obtengamos tu ubicación.");
      return;
    }
    if (!matricula) {
        Alert.alert("Error", "La matrícula no puede estar vacía.");
        return;
    }

    setLoading(true);
    try {
      // Recuperar el token de sesion para autorizacion
      const token = await SecureStore.getItemAsync('user_token');

      // Crear el payload para enviar a la API con los datos necesarios (matricula y ubicacion)
      const payload = {
        matricula: matricula, 
        latitud: location.latitude,
        longitud: location.longitude
      };

      // Log para debug
      console.log("Enviando a Java:", payload);

      // Llamada a la API de Java para registrar la incidencia
      await springApi.post('/incidencias', payload, {
        headers: { Authorization: `Bearer ${token}` }
      });


      // Mensaje de exito y volver al inicio
      Alert.alert("¡Éxito!", "Incidencia registrada correctamente", [
        { text: "OK", onPress: () => navigation.popToTop() } 
      ]);

    } catch (error) {
      // Manejar errores de la API con mensajes adecuados
      
      if (error.response) {
        // El servidor respondió con un código de error
        const data = error.response.data;
        const status = error.response.status;
        
        // CASO 1: Error de Negocio Esperado (404 con mensaje personalizado)
        if (status === 404 && data && data.mensaje) {
             console.log("Validación de negocio:", data.mensaje); 
             Alert.alert("No se pudo registrar", data.mensaje); 
        } 
        // CASO 2: Otros errores del servidor 
        else if (status === 403) {
             console.log("Acceso denegado (403)");
             Alert.alert("Acceso Denegado", "Tu sesión ha expirado o no tienes permisos.");
        } 
        else {
             // Error 500 u otros no esperados
             console.error("Error del servidor:", error);
             Alert.alert("Error del Servidor", "Ocurrió un problema técnico. Intenta más tarde.");
        }
      } else if (error.request) {
        // No hubo respuesta (Servidor apagado o sin conexion)
        console.error("Error de conexión:", error.message);
        Alert.alert("Error de Conexión", "No se pudo conectar con el servidor. Verifica tu internet.");
      } else {
        // Error al configurar la petición
        console.error("Error inesperado:", error);
        Alert.alert("Error", "Ocurrió un error inesperado en la aplicación.");
      }

    } finally {
      // Desactivar estado de carga
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Confirmar Datos</Text>

      {/* Foto de referencia de la matricula*/}
      <Image source={{ uri: fotoUri }} style={styles.imagePreview} />

      <View style={styles.form}>
        <Text style={styles.label}>Matrícula Detectada:</Text>
        <TextInput
          style={styles.input}
          value={matricula}
          onChangeText={setMatricula}
          editable={false}
          autoCapitalize="characters"
        />

        <Text style={styles.label}>Ubicación:</Text>
        <Text style={styles.coords}>
          {location ? `${location.latitude.toFixed(5)}, ${location.longitude.toFixed(5)}` : "Obteniendo..."}
        </Text>

        <TouchableOpacity 
            style={[styles.button, (!location || loading) && styles.buttonDisabled]} 
            onPress={confirmarIncidencia}
            disabled={!location || loading}
        >
          <Text style={styles.buttonText}>{loading ? "Enviando..." : "Registrar Multa"}</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

// Estilos
const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 20, alignItems: 'center', backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  imagePreview: { width: 200, height: 100, borderRadius: 10, marginBottom: 20, resizeMode: 'cover' },
  form: { width: '100%' },
  label: { fontSize: 16, fontWeight: '600', marginBottom: 5, color: '#555' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 15, borderRadius: 8, fontSize: 20, marginBottom: 20, backgroundColor: '#f9f9f9', fontWeight: 'bold', textAlign: 'center' },
  coords: { fontSize: 14, color: '#888', marginBottom: 30, textAlign: 'center' },
  button: { backgroundColor: '#e74c3c', padding: 15, borderRadius: 10, alignItems: 'center' },
  buttonDisabled: { backgroundColor: '#ffbaba' },
  buttonText: { color: 'white', fontSize: 18, fontWeight: 'bold' },
});