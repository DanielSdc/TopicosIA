package com.topai.incidenciasestacionamiento.service;

import com.topai.incidenciasestacionamiento.dto.request.UsuarioRequestDTO;
import com.topai.incidenciasestacionamiento.dto.response.UsuarioResponseDTO;
import com.topai.incidenciasestacionamiento.exception.NotFoundException;
import com.topai.incidenciasestacionamiento.mapper.Mapper;
import com.topai.incidenciasestacionamiento.model.Usuario;
import com.topai.incidenciasestacionamiento.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Servicio para la gestión de usuarios.
 * Se implementa la logística de negocio relacionada con los usuarios
 * {@link Usuario}.
 */

@Service
public class UsuarioService {

    @Autowired
    UsuarioRepository usuarioRepository;

    /**
     * Registrar un nuevo usuario.
     * @param usuarioDTO datos del usuario a registrar
     * @return UsuarioResponseDTO con los datos del usuario registrado
     * @throws RuntimeException si el correo ya está registrado
     */
    public UsuarioResponseDTO registrarUsuario(UsuarioRequestDTO usuarioDTO) {
        if (usuarioRepository.findByCorreo(usuarioDTO.getCorreo()).isPresent()) {
            throw new RuntimeException("El correo ya está registrado");
        }

        Usuario usuario = Usuario.builder()
                .nombre(usuarioDTO.getNombre())
                .correo(usuarioDTO.getCorreo())
                .password("FIREBASE_MANAGED")
                .role("ROLE_USER")
                .build();

        return Mapper.toDTO(usuarioRepository.save(usuario));
    }

    /**
     * Buscar un usuario por su correo electrónico.
     * @param correo correo del usuario a buscar
     * @return UsuarioResponseDTO con los datos del usuario encontrado
     * @throws NotFoundException si no se encuentra el usuario con el correo
     *                           proporcionado
     */
    public UsuarioResponseDTO buscarPorCorreo(String correo) {
        Usuario usuario = usuarioRepository.findByCorreo(correo)
                .orElseThrow(() -> new NotFoundException("Usuario con correo " + correo + " no encontrado"));
        return Mapper.toDTO(usuario);
    }

}
