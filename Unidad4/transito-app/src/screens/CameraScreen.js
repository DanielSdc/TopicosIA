import React, { useState, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert, ActivityIndicator } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { pythonApi } from '../config/api';

export default function CameraScreen({ navigation }) {
  const [permission, requestPermission] = useCameraPermissions();
  const [uploading, setUploading] = useState(false);
  const cameraRef = useRef(null);

  if (!permission) {
    return <View />; 
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.text}>Necesitamos permiso para usar la cámara</Text>
        <TouchableOpacity onPress={requestPermission} style={styles.button}>
          <Text style={styles.buttonText}>Dar Permiso</Text>
        </TouchableOpacity>
      </View>
    );
  }
  // Funcion asincrona para tomar la foto y enviarla a la API de Python
  const tomarFoto = async () => {
    if (!cameraRef.current) return;
    
    try {
      setUploading(true);
      
      // Tomar la foto bajo calidad media para reducir tamaño
      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.5,
        base64: false,
      });

      // Preparar la imagen para enviarla a la API
      const formData = new FormData();
      formData.append('file', {
        uri: photo.uri,
        type: 'image/jpeg',
        name: 'placa.jpg',
      });

      console.log("Enviando a Python ANPR..."); // Log para debug
      
      // Llamada a la API de Python
      const response = await pythonApi.post('/read_plate', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setUploading(false); // Actualizar estado de carga

      // Procesar la respuesta (asumiendo que devuelve un solo parametro: { plate_text: "ABC123" })
      const placaDetectada = response.data.plate_text; 

      // Navegar a la pantalla de Confirmación con la matrícula detectada
      if (placaDetectada && placaDetectada.trim() !== "") {
        navigation.navigate('Confirm', { 
          matriculaDetectada: placaDetectada,
          fotoUri: photo.uri 
        });
      } else {
        // No se detectó matrícula
        // Mensaje de error y opcion para reintentar
        Alert.alert(
            "No se detectó matrícula", 
            "La API no encontró texto legible. Intenta acercarte más.",
            [
                { text: "Cancelar", style: "cancel", onPress: () => navigation.goBack() },
                { text: "Reintentar", onPress: () => {} }
            ]
        );
      }
      // Manejar errores de la API
    } catch (error) {
      setUploading(false);
      console.error("Error API Python:", error);
      Alert.alert("Error", "No se pudo conectar con el servicio de lectura de placas.");
    }
  };

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} facing="back" ref={cameraRef}>
        <View style={styles.buttonContainer}>
          {uploading ? (
            <ActivityIndicator size="large" color="#fff" />
          ) : (
            <TouchableOpacity style={styles.captureButton} onPress={tomarFoto}>
              <View style={styles.innerCircle} />
            </TouchableOpacity>
          )}
        </View>
      </CameraView>
    </View>
  );
}

// Estilos
const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center' },
  camera: { flex: 1 },
  text: { textAlign: 'center', fontSize: 18, marginBottom: 20 },
  button: { backgroundColor: '#007bff', padding: 15, borderRadius: 10, alignSelf: 'center' },
  buttonText: { color: 'white', fontSize: 16 },
  buttonContainer: { flex: 1, flexDirection: 'row', backgroundColor: 'transparent', margin: 64, justifyContent: 'center', alignItems: 'flex-end' },
  captureButton: { width: 70, height: 70, borderRadius: 35, backgroundColor: 'rgba(255,255,255,0.3)', justifyContent: 'center', alignItems: 'center' },
  innerCircle: { width: 60, height: 60, borderRadius: 30, backgroundColor: 'white' },
});