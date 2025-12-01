import React, { useState, useCallback } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator, RefreshControl, TouchableOpacity } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { springApi } from '../config/api';
import { useFocusEffect } from '@react-navigation/native';

export default function MisIncidenciasScreen() {
  const [incidencias, setIncidencias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  // Estado para controlar qué pestaña selecciona el usuario ('recibidas' | 'enviadas')
  const [activeTab, setActiveTab] = useState('recibidas');

  const fetchIncidencias = async () => {
    try {
      setLoading(true);
      const token = await SecureStore.getItemAsync('user_token');
      if (!token) return;

      // Determinamos el endpoint según la pestaña activa
      // recibidas = Reportes hacia mí (endpoint actual)
      // enviadas = Reportes que yo hice (endpoint nuevo)
      const endpoint = activeTab === 'recibidas' 
        ? '/incidencias/recibidas' 
        : '/incidencias/enviadas';

      const response = await springApi.get(endpoint, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setIncidencias(response.data);
    } catch (error) {
      console.error("Error cargando incidencias:", error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Recargar datos cuando cambia la pestaña 
  useFocusEffect(
    useCallback(() => {
      fetchIncidencias();
    }, [activeTab]) 
  );
  
  const onRefresh = () => {
    setRefreshing(true);
    fetchIncidencias();
  };

  // Formatear fecha para mostrar
  const formatDate = (dateString) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Renderizado de cada tarjeta de incidencia
  const renderItem = ({ item }) => {
    // Personalizar la tarjeta si es enviada o recibida
    const isReceived = activeTab === 'recibidas';
    const cardColor = isReceived ? '#e74c3c' : '#3498db'; // Rojo para reportes recibidos, azul para reportes hechos
    const icon = isReceived ? '🚨' : '📝';
    const title = isReceived ? `Infracción #${item.id}` : `Reporte #${item.id}`;

    return (
      <View style={[styles.card, { borderLeftColor: cardColor }]}>
        <View style={styles.cardHeader}>
          <Text style={styles.icon}>{icon}</Text>
          <View>
            <Text style={[styles.cardTitle, { color: cardColor }]}>{title}</Text>
            <Text style={styles.date}>{formatDate(item.fecha)}</Text>
          </View>
        </View>
        
        <View style={styles.divider} />
        
        <View style={styles.row}>
          <Text style={styles.label}>Vehículo:</Text>
          <Text style={styles.value}>{item.automovil?.marca || 'Desconocido'} {item.automovil?.modelo || ''}</Text>
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Matricula:</Text>
          <Text style={styles.value}>{item.automovil?.matricula || 'Desconocido'}</Text>
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Ubicación:</Text>
          <Text style={styles.value}>
              {item.latitud.toFixed(4)}, {item.longitud.toFixed(4)}
          </Text>
        </View>

        {/* Dato extra: Si es recibida, mostramos quién reportó (si el backend lo manda) aunque no es lo ideal para un entorno real*/}
        {isReceived && item.usuario && (
           <View style={styles.row}>
             <Text style={styles.label}>Reportado por:</Text>
             <Text style={styles.value}>{item.usuario.nombre || 'Agente'}</Text>
           </View>
        )}
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {/* seccion de pestañas */}
      <View style={styles.tabContainer}>
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'recibidas' && styles.activeTab]} 
          onPress={() => setActiveTab('recibidas')}
        >
          <Text style={[styles.tabText, activeTab === 'recibidas' && styles.activeTabText]}>
            Recibidas
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={[styles.tab, activeTab === 'enviadas' && styles.activeTab]} 
          onPress={() => setActiveTab('enviadas')}
        >
          <Text style={[styles.tabText, activeTab === 'enviadas' && styles.activeTabText]}>
            Enviadas
          </Text>
        </TouchableOpacity>
      </View>

      {/* lista de contenido */}
      {loading && !refreshing ? (
        <ActivityIndicator size="large" color="#3498db" style={styles.center} />
      ) : (
        incidencias.length > 0 ? (
          <FlatList
            data={incidencias}
            keyExtractor={(item) => item.id.toString()}
            refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
            renderItem={renderItem}
            contentContainerStyle={styles.listContent}
          />
        ) : (
          <View style={styles.emptyState}>
            <Text style={styles.emptyEmoji}>
              {activeTab === 'recibidas' ? '👍' : '📭'}
            </Text>
            <Text style={styles.emptyTitle}>
              {activeTab === 'recibidas' ? 'Sin Infracciones' : 'Sin Reportes'}
            </Text>
            <Text style={styles.emptyText}>
              {activeTab === 'recibidas' 
                ? 'No tienes reportes registrados en tu contra.' 
                : 'Aún no has enviado ningún reporte de incidencia.'}
            </Text>
          </View>
        )
      )}
    </View>
  );
}

// Estilos
const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f7fa' },
  center: { flex: 1, justifyContent: 'center' },
  listContent: { padding: 20 },

  tabContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    padding: 5,
    margin: 15,
    borderRadius: 10,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 }, 
    shadowOpacity: 0.1, 
    shadowRadius: 1,
  },
  tab: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
    borderRadius: 8,
  },
  activeTab: {
    backgroundColor: '#3498db', 
  },
  tabText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#7f8c8d',
  },
  activeTabText: {
    color: '#fff',
    fontWeight: 'bold',
  },

  card: { 
    backgroundColor: 'white', 
    padding: 15, 
    borderRadius: 12, 
    marginBottom: 15, 
    elevation: 3, 
    shadowColor: '#000', 
    shadowOffset: { width: 0, height: 2 }, 
    shadowOpacity: 0.1, 
    shadowRadius: 4, 
    borderLeftWidth: 5 
  },
  cardHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  icon: { fontSize: 24, marginRight: 10 },
  cardTitle: { fontSize: 18, fontWeight: 'bold' },
  date: { fontSize: 12, color: '#7f8c8d' },
  divider: { height: 1, backgroundColor: '#ecf0f1', marginBottom: 10 },

  row: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 5 },
  label: { fontWeight: '600', color: '#555' },
  value: { color: '#333' },

  emptyState: { alignItems: 'center', marginTop: 80 },
  emptyEmoji: { fontSize: 50, marginBottom: 10 },
  emptyTitle: { fontSize: 20, fontWeight: 'bold', color: '#2c3e50' },
  emptyText: { color: '#7f8c8d', marginTop: 5, paddingHorizontal: 40, textAlign: 'center' }
});