import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import React, { useState } from 'react';
import { Alert, Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';

interface ProfilePhotoPickerProps {
  currentPhoto: string | null;
  onPhotoChange: (photo: string) => void;
}

export default function ProfilePhotoPicker({ currentPhoto, onPhotoChange }: ProfilePhotoPickerProps) {
  const [photoUri, setPhotoUri] = useState(currentPhoto);

  // Solicitar permissões
  const requestPermissions = async () => {
    const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
    const { status: libraryStatus } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    
    if (cameraStatus !== 'granted' || libraryStatus !== 'granted') {
      Alert.alert('Permissão Necessária', 'Precisamos de permissão para acessar suas fotos.');
      return false;
    }
    return true;
  };

  // Escolher foto da galeria
  const pickImageFromLibrary = async () => {
    const hasPermission = await requestPermissions();
    if (!hasPermission) return;

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.7,
      base64: true,
    });

    if (!result.canceled && result.assets[0]) {
      const base64Image = `data:image/jpeg;base64,${result.assets[0].base64}`;
      setPhotoUri(base64Image);
      onPhotoChange(base64Image);
    }
  };

  // Tirar foto com a câmera
  const takePhoto = async () => {
    const hasPermission = await requestPermissions();
    if (!hasPermission) return;

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.7,
      base64: true,
    });

    if (!result.canceled && result.assets[0]) {
      const base64Image = `data:image/jpeg;base64,${result.assets[0].base64}`;
      setPhotoUri(base64Image);
      onPhotoChange(base64Image);
    }
  };

  // Mostrar opções
  const showPhotoOptions = () => {
    Alert.alert(
      'Foto de Perfil',
      'Escolha uma opção',
      [
        { text: 'Tirar Foto', onPress: takePhoto },
        { text: 'Escolher da Galeria', onPress: pickImageFromLibrary },
        { text: 'Cancelar', style: 'cancel' },
      ],
      { cancelable: true }
    );
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={showPhotoOptions} style={styles.photoContainer}>
        {photoUri ? (
          <Image source={{ uri: photoUri }} style={styles.photo} />
        ) : (
          <View style={styles.placeholderContainer}>
            <Ionicons name="person" size={60} color="#999" />
          </View>
        )}
        <View style={styles.editButton}>
          <Ionicons name="camera" size={20} color="#fff" />
        </View>
      </TouchableOpacity>
      <Text style={styles.label}>Toque para alterar a foto</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginVertical: 20,
  },
  photoContainer: {
    position: 'relative',
    width: 120,
    height: 120,
    borderRadius: 60,
    overflow: 'hidden',
    backgroundColor: '#f0f0f0',
    borderWidth: 3,
    borderColor: '#6C47FF',
  },
  photo: {
    width: '100%',
    height: '100%',
  },
  placeholderContainer: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#e0e0e0',
  },
  editButton: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    backgroundColor: '#6C47FF',
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#fff',
  },
  label: {
    marginTop: 10,
    fontSize: 14,
    color: '#666',
  },
});