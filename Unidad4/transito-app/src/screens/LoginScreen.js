import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  Alert, 
  ActivityIndicator 
} from 'react-native';
import { auth } from '../config/firebase'; 
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';
import * as SecureStore from 'expo-secure-store';
import { springApi } from '../config/api';

// Pantalla de Login y Registro
export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [nombre, setNombre] = useState('');
  
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!auth) {
      Alert.alert("Error de Configuración", "Firebase no se pudo inicializar.");
    }
  }, []);

  // Manejar Login o Registro
  const handleAuth = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Por favor completa todos los campos');
      return;
    }

    if (!auth) {
        Alert.alert("Error", "No hay conexión con el servicio de autenticación.");
        return;
    }

    setLoading(true);
    try {
      let userCredential;

      if (isLogin) {
        // Login
        userCredential = await signInWithEmailAndPassword(auth, email, password);
      } else {
        // Registro
        if (!nombre) {
            Alert.alert('Error', 'El nombre es obligatorio para registrarse');
            setLoading(false);
            return;
        }
        userCredential = await createUserWithEmailAndPassword(auth, email, password);
      }

      const user = userCredential.user;
      const token = await user.getIdToken();

      // Guardar sesión
      await SecureStore.setItemAsync('user_token', token);
      await SecureStore.setItemAsync('user_email', email);

      // Sincronizar con API de Java (Solo en registro)
      if (!isLogin) {
        await registrarEnBackend(nombre, email, token);
      }

      setLoading(false);
      
      // redireccionar a Home
      navigation.replace('Home'); 

    } catch (error) {
      // Manejar errores de autenticación
      setLoading(false);
      console.error("Error Auth:", error);
      let msg = error.message;
      if (msg.includes('auth/invalid-credential')) msg = 'Credenciales incorrectas';
      if (msg.includes('auth/email-already-in-use')) msg = 'El correo ya está registrado';
      if (msg.includes('auth/weak-password')) msg = 'La contraseña es muy débil (mínimo 6 caracteres)';
      
      Alert.alert('Error', msg);
    }
  };

  // Función para registrar el usuario en el backend de Java
  const registrarEnBackend = async (nombre, email, token) => {
    try {
      console.log("Enviando datos a Spring Boot...");
      await springApi.post('/usuarios/registrar', {
        nombre: nombre,
        correo: email
      }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      console.log("Usuario sincronizado en Postgres");
    } catch (error) {
      console.error("Error Backend:", error);
  
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{isLogin ? 'Iniciar Sesión' : 'Crear Cuenta'}</Text>

      {!isLogin && (
        <TextInput
          style={styles.input}
          placeholder="Nombre Completo"
          value={nombre}
          onChangeText={setNombre}
        />
      )}

      <TextInput
        style={styles.input}
        placeholder="Correo Electrónico"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
      />

      <TextInput
        style={styles.input}
        placeholder="Contraseña"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      {loading ? (
        <ActivityIndicator size="large" color="#007bff" style={{ marginTop: 20 }} />
      ) : (
        <TouchableOpacity style={styles.button} onPress={handleAuth}>
          <Text style={styles.buttonText}>{isLogin ? 'Entrar' : 'Registrarse'}</Text>
        </TouchableOpacity>
      )}

      <TouchableOpacity onPress={() => setIsLogin(!isLogin)} style={{ marginTop: 20 }}>
        <Text style={styles.switchText}>
          {isLogin ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia Sesión'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}

// Estilos
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 30,
    textAlign: 'center',
    color: '#333',
  },
  input: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  button: {
    backgroundColor: '#007bff',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  switchText: {
    textAlign: 'center',
    color: '#007bff',
    marginTop: 10,
  },
});