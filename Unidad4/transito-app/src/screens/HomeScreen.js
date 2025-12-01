import React, { useState, useCallback } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert, ActivityIndicator, RefreshControl, ScrollView } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { useFocusEffect } from '@react-navigation/native';
import { springApi } from '../config/api';

export default function HomeScreen({ navigation }) {
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  // Funcion asincrona para cargar el perfil completo desde la API
  const fetchProfile = async () => {
    try {
      const token = await SecureStore.getItemAsync('user_token');
      if (!token) return;

      const response = await springApi.get('/usuarios/perfil', {
        headers: { Authorization: `Bearer ${token}` }
      });

      setUserProfile(response.data);
    } catch (error) {
      console.error("Error cargando perfil:", error);
      // Si falla la carga del perfil por autorizacion se cierra sesion
      if (error.response?.status === 403) {
        handleLogout();
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };
  // Cargar datos cada vez que la pantalla gana foco
  useFocusEffect(
    useCallback(() => {
      fetchProfile();
    }, [])
  );

  const onRefresh = () => {
    setRefreshing(true);
    fetchProfile();
  };

  // Funcion para cerrar sesion
  const handleLogout = async () => {
    try {
      await SecureStore.deleteItemAsync('user_token');
      await SecureStore.deleteItemAsync('user_email');
      
      navigation.reset({
        index: 0,
        routes: [{ name: 'Login' }],
      });
    } catch (error) {
      console.error("Error al cerrar sesión", error);
    }
  };

  // Renderizado condicional del estado de la tarjetaPase
  // 3 casos:
  // A. No es propietario -> Mostrar aviso para vincular con perfil de propietario
  // B. Es propietario y tarjetaPase=true -> Mostrar tarjeta habilitada
  // C. Es propietario y tarjetaPase=false -> Mostrar tarjeta deshabilitada
  const renderStatusCard = () => {
    if (!userProfile) return null;

    const propietario = userProfile.propietario;

    // CASO A: No es propietario (Null)
    if (!propietario) {
      return (
        <TouchableOpacity 
          style={[styles.statusCard, styles.statusWarning]}
          onPress={() => navigation.navigate('MisVehiculos')} // Opciones para vincular con perfil de propietario
        >
          <Text style={styles.statusIcon}>⚠️</Text>
          <View>
            <Text style={styles.statusTitle}>Tarjeta de pase no vinculada</Text>
            <Text style={styles.statusSubtitle}>Toca aquí para vincular tu perfil de propietario</Text>
          </View>
        </TouchableOpacity>
      );
    }

    // CASO B: Es propietario, verificamos tarjetaPase
    // Subcaso B1: tarjetaPase=true
    if (propietario.tarjetaPase) {
      return (
        <View style={[styles.statusCard, styles.statusSuccess]}>
          <Text style={styles.statusIcon}>✅</Text>
          <View>
            <Text style={styles.statusTitle}>Tarjeta Habilitada</Text>
            <Text style={styles.statusSubtitle}>Tu acceso está activo</Text>
          </View>
        </View>
      );
    } else {
      // Subcaso B2: tarjetaPase=false
      return (
        <View style={[styles.statusCard, styles.statusError]}>
          <Text style={styles.statusIcon}>⛔</Text>
          <View>
            <Text style={styles.statusTitle}>Tarjeta Deshabilitada</Text>
            <Text style={styles.statusSubtitle}>Contacta a administración</Text>
          </View>
        </View>
      );
    }
  };

  // Renderizado principal
  if (loading && !refreshing) {
    return (
      <View style={[styles.container, styles.center]}>
        <ActivityIndicator size="large" color="#3498db" />
      </View>
    );
  }

  // Renderizado principal
  return (
    <ScrollView 
      contentContainerStyle={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <View style={styles.header}>
        <Text style={styles.welcomeText}>Bienvenido,</Text>
        <Text style={styles.userName}>{userProfile?.nombre || 'Usuario'}</Text>
      </View>

      {/* sección de estado de la tarjetaPase */}
      <View style={styles.statusSection}>
        {renderStatusCard()}
      </View>

      <View style={styles.menu}>
        {/* Opciones del menú principal */}
        {/* boton 1: Reportar Incidencia */}
        <TouchableOpacity 
          style={[styles.card, styles.actionCard]} 
          onPress={() => navigation.navigate('Camera')} 
        >
          <Text style={styles.cardIcon}>📷</Text>
          <View>
            <Text style={styles.cardTitle}>Reportar Incidencia</Text>
            <Text style={styles.cardText}>Escanear placa y generar reporte</Text>
          </View>
        </TouchableOpacity>

        {/* boton 2: mostrar vehiculos del usuario/propietario */}
        <TouchableOpacity 
          style={[styles.card, styles.infoCard]}
          onPress={() => navigation.navigate('MisVehiculos')} 
        >
          <Text style={styles.cardIcon}>🚗</Text>
          <View>
            <Text style={styles.cardTitle}>Mis Vehículos</Text>
            <Text style={styles.cardText}>Ver mis automoviles registrados</Text>
          </View>
        </TouchableOpacity>

        {/* boton 3: Ver incidencias recibidas/enviadas */}
        <TouchableOpacity 
          style={[styles.card, styles.alertCard]}
          onPress={() => navigation.navigate('MisIncidencias')} 
        >
          <Text style={styles.cardIcon}>🚨</Text>
          <View>
            <Text style={styles.cardTitle}>Infracciones</Text>
            <Text style={styles.cardText}>Ver reportes recibidos y enviados</Text>
          </View>
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutText}>Cerrar Sesión</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

// Estilos
const styles = StyleSheet.create({
  container: { 
    flexGrow: 1, 
    padding: 20, 
    backgroundColor: '#f5f7fa' 
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  },
  header: {
    marginTop: 40,
    marginBottom: 20,
  },
  welcomeText: {
    fontSize: 16,
    color: '#7f8c8d',
  },
  userName: { 
    fontSize: 28, 
    fontWeight: 'bold', 
    color: '#2c3e50',
  },
  
  statusSection: {
    marginBottom: 30,
  },
  statusCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderRadius: 12,
    borderWidth: 1,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  statusIcon: {
    fontSize: 24,
    marginRight: 15,
  },
  statusTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 2,
  },
  statusSubtitle: {
    fontSize: 13,
  },
  statusWarning: {
    backgroundColor: '#fff3cd',
    borderColor: '#ffeeba',
  },
  statusSuccess: {
    backgroundColor: '#d4edda',
    borderColor: '#c3e6cb',
  },
  statusError: {
    backgroundColor: '#f8d7da',
    borderColor: '#f5c6cb',
  },

  menu: { 
    gap: 20 
  },
  card: { 
    padding: 20, 
    borderRadius: 15, 
    elevation: 4, 
    shadowColor: '#000', 
    shadowOffset: { width: 0, height: 2 }, 
    shadowOpacity: 0.1, 
    shadowRadius: 4,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 15
  },
  cardIcon: {
    fontSize: 30
  },
  actionCard: { 
    backgroundColor: '#ffffff',
    borderLeftWidth: 5,
    borderLeftColor: '#3498db'
  },
  infoCard: { 
    backgroundColor: '#ffffff',
    borderLeftWidth: 5,
    borderLeftColor: '#2ecc71'
  },
  cardTitle: { 
    fontSize: 18, 
    fontWeight: 'bold', 
    color: '#34495e', 
    marginBottom: 2 
  },
  cardText: { 
    color: '#95a5a6',
    fontSize: 13
  },
  logoutButton: { 
    marginTop: 40, 
    alignSelf: 'center', 
    paddingVertical: 10, 
    paddingHorizontal: 30
  },
  logoutText: { 
    color: '#c0392b', 
    fontWeight: 'bold',
    fontSize: 16
  }
});