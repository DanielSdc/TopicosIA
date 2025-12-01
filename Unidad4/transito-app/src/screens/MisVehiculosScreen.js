import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, FlatList, TextInput, TouchableOpacity, Alert, StyleSheet, ActivityIndicator, RefreshControl } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { springApi } from '../config/api';
import { useFocusEffect } from '@react-navigation/native';

export default function MisVehiculosScreen() {
  const [autos, setAutos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  // Estado para la vinculación (Formulario) con el ID de propietario
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [idPropietarioInput, setIdPropietarioInput] = useState('');

  // Mostrar vehiculos
  const fetchMisAutos = async () => {
    try {
      const token = await SecureStore.getItemAsync('user_token');
      if (!token) return;

      // Llamada al endpoint que devuelve los autos del usuario
      const response = await springApi.get('/automoviles/mis-autos', {
        headers: { Authorization: `Bearer ${token}` }
      });

      setAutos(response.data);
    } catch (error) {
      console.error("Error cargando autos:", error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  useFocusEffect(
    useCallback(() => {
      fetchMisAutos();
    }, [])
  );
  const onRefresh = () => {
    setRefreshing(true);
    fetchMisAutos();
  };

  //Función para Vincular Cuenta de usuario con un propietario mediante ID
  const vincularCuenta = async () => {
    if (!idPropietarioInput) {
      Alert.alert("Error", "Por favor ingresa tu ID de propietario");
      return;
    }

    // Llamada a la API para vincular el propietario
    try {
      setLoading(true);
      const token = await SecureStore.getItemAsync('user_token');
      
      await springApi.post(
        `/propietarios/${idPropietarioInput}/vincular`, 
        {}, 
        { headers: { Authorization: `Bearer ${token}` } }
      );

      Alert.alert("¡Éxito!", "Cuenta vinculada correctamente.");
      setMostrarFormulario(false);
      fetchMisAutos(); // Recargar la lista con autos vinculados
      
    } catch (error) {
      console.error(error);
      Alert.alert("Error", "No se pudo encontrar ese propietario o ya está vinculado.");
    } finally {
      setLoading(false);
    }
  };

  if (loading && !refreshing) return <ActivityIndicator size="large" color="#0000ff" style={styles.center} />;

  return (
    <View style={styles.container}>
      
      {autos.length > 0 ? (
        <FlatList
          data={autos}
          keyExtractor={(item) => item.id.toString()}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          contentContainerStyle={{ paddingBottom: 20 }}
          renderItem={({ item }) => (
            
            <View style={styles.card}>
              {/* Mostrar datos del vehiculo */}
              <View style={styles.cardHeader}>
                <Text style={styles.label}>Matrícula:</Text>
                <Text style={styles.value}>{item.matricula}</Text>
              </View>
              <View style={styles.divider} />
              <Text style={styles.label}>Marca:</Text>
              <Text style={styles.value}>{item.marca}</Text>
              <Text style={styles.label}>Modelo:</Text>
              <Text style={styles.value}>{item.modelo}</Text>
              <Text style={styles.label}>Año:</Text>
              <Text style={styles.value}>{item.year}</Text>
              <Text style={styles.label}>Propietario:</Text>
              {/* Mostrar propietario */}
              <Text style={styles.value}>{item.propietario ? item.propietario.nombre : 'Desconocido'}</Text>
              
              <Text style={styles.label}>Dirección:</Text>
              <Text style={styles.value}>{item.propietario ? item.propietario.direccion : 'N/A'}</Text>
            </View>
          )}
        />
      ) : (
        //  En caso de no tener autos vinculados
        <View style={styles.emptyState}>
          <Text style={styles.emptyEmoji}>📂</Text>
          <Text style={styles.emptyTitle}>No hay vehículos</Text>
          <Text style={styles.emptyText}>No se encontraron vehículos asociados a tu cuenta de usuario.</Text>
          
          {!mostrarFormulario ? (
            <TouchableOpacity style={styles.mainButton} onPress={() => setMostrarFormulario(true)}>
              <Text style={styles.buttonText}>Vincular Cuenta de Propietario</Text>
            </TouchableOpacity>
          ) : (
            // Formulario de vinculación
            <View style={styles.formContainer}>
              <Text style={styles.formLabel}>Ingresa tu ID de Propietario:</Text>
              <Text style={styles.formSubLabel}>(Este ID se te proporcionara en la oficina de servicios escolares)</Text>
              
              <TextInput 
                style={styles.input} 
                placeholder="Ej: 1" 
                keyboardType="numeric"
                value={idPropietarioInput}
                onChangeText={setIdPropietarioInput}
                autoFocus={true}
              />
              
              <View style={styles.row}>
                 <TouchableOpacity style={[styles.smallButton, styles.cancelButton]} onPress={() => setMostrarFormulario(false)}>
                  <Text style={styles.smallButtonText}>Cancelar</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.smallButton} onPress={vincularCuenta}>
                  <Text style={styles.smallButtonText}>Confirmar</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </View>
      )}
    </View>
  );
}

// Estilos
const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f5f7fa' },
  center: { flex: 1, justifyContent: 'center' },

  card: { backgroundColor: 'white', padding: 20, borderRadius: 15, marginBottom: 15, elevation: 3, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4 },
  cardHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  cardIcon: { fontSize: 24, marginRight: 10 },
  matricula: { fontSize: 22, fontWeight: 'bold', color: '#2c3e50' },
  divider: { height: 1, backgroundColor: '#ecf0f1', marginBottom: 10 },
  label: { fontSize: 12, color: '#7f8c8d', marginTop: 5, textTransform: 'uppercase', letterSpacing: 0.5 },
  value: { fontSize: 16, color: '#34495e', fontWeight: '500' },

  emptyState: { alignItems: 'center', justifyContent: 'center', marginTop: 60 },
  emptyEmoji: { fontSize: 50, marginBottom: 20 },
  emptyTitle: { fontSize: 20, fontWeight: 'bold', color: '#2c3e50', marginBottom: 10 },
  emptyText: { fontSize: 15, color: '#7f8c8d', textAlign: 'center', marginBottom: 30, paddingHorizontal: 20 },

  mainButton: { backgroundColor: '#3498db', paddingVertical: 15, paddingHorizontal: 30, borderRadius: 25, elevation: 2 },
  buttonText: { color: 'white', fontWeight: 'bold', fontSize: 16 },

  formContainer: { width: '100%', backgroundColor: 'white', padding: 20, borderRadius: 15, elevation: 4 },
  formLabel: { fontSize: 16, fontWeight: 'bold', color: '#2c3e50' },
  formSubLabel: { fontSize: 12, color: '#95a5a6', marginBottom: 15 },
  input: { borderWidth: 1, borderColor: '#bdc3c7', padding: 12, borderRadius: 8, marginBottom: 20, fontSize: 16, backgroundColor: '#f9f9f9' },

  row: { flexDirection: 'row', justifyContent: 'space-between', gap: 10 },
  smallButton: { flex: 1, backgroundColor: '#2ecc71', padding: 12, borderRadius: 8, alignItems: 'center' },
  cancelButton: { backgroundColor: '#e74c3c' },
  smallButtonText: { color: 'white', fontWeight: 'bold' }
});