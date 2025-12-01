import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { LogBox } from 'react-native';

// Ignorar logs de Firebase
LogBox.ignoreLogs(['Analytics: Firebase Analytics is not supported']);

// Importar Pantallas
import LoginScreen from './src/screens/LoginScreen';
import HomeScreen from './src/screens/HomeScreen';
import CameraScreen from './src/screens/CameraScreen';
import ConfirmScreen from './src/screens/ConfirmScreen';
import MisVehiculosScreen from './src/screens/MisVehiculosScreen';
import MisIncidenciasScreen from './src/screens/MisIncidenciasScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen 
          name="Login" 
          component={LoginScreen} 
          options={{ headerShown: false }} 
        />
        <Stack.Screen 
          name="Home" 
          component={HomeScreen} 
          options={{ headerShown: false }} 
        />
        <Stack.Screen 
          name="Camera" 
          component={CameraScreen} 
          options={{ title: 'Escanear Placa' }} 
        />
        <Stack.Screen 
          name="Confirm" 
          component={ConfirmScreen} 
          options={{ title: 'Confirmar Incidencia' }} 
        />
        <Stack.Screen 
          name="MisVehiculos" 
          component={MisVehiculosScreen} 
          options={{ title: 'Mis Vehículos' }} 
        />
        <Stack.Screen 
          name="MisIncidencias" 
          component={MisIncidenciasScreen} 
          options={{ title: 'Mis Incidencias' }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}