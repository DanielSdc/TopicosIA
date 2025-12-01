package com.topai.incidenciasestacionamiento.service;

import com.topai.incidenciasestacionamiento.dto.request.PropietarioRequestDTO;
import com.topai.incidenciasestacionamiento.dto.response.PropietarioResponseDTO;
import com.topai.incidenciasestacionamiento.exception.NotFoundException;
import com.topai.incidenciasestacionamiento.mapper.Mapper;
import com.topai.incidenciasestacionamiento.model.Propietario;
import com.topai.incidenciasestacionamiento.model.Usuario;
import com.topai.incidenciasestacionamiento.repository.IncidenciaRepository;
import com.topai.incidenciasestacionamiento.repository.PropietarioRepository;
import com.topai.incidenciasestacionamiento.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Servicio para la gestión de propietarios.
 * Se implementa la logística de negocio relacionada con los propietarios
 * {@link Propietario}.
 */
@Service
public class PropietarioService {

    @Autowired
    PropietarioRepository propietarioRepository;

    @Autowired
    UsuarioRepository usuarioRepository;

    @Autowired
    IncidenciaRepository incidenciaRepository;

    /**
     * Registrar un nuevo propietario.
     * @param propietarioDTO datos del propietario a registrar
     * @return PropietarioResponseDTO con los datos del propietario registrado
     */
    public PropietarioResponseDTO registrarPropietario(PropietarioRequestDTO propietarioDTO) {
        Propietario propietario = Propietario.builder()
                .nombre(propietarioDTO.getNombre())
                .direccion(propietarioDTO.getNombre())
                .tarjetaPase(true)
                .build();
        if (propietarioDTO.getUsuarioId() != null) {
            Usuario usuario = usuarioRepository.findById(propietarioDTO.getUsuarioId())
                    .orElseThrow(() -> new NotFoundException("Usuario no encontrado para vincular con propietario"));
            propietario.setUsuario(usuario);
        }

        return Mapper.toDTO(propietarioRepository.save(propietario));
    }

    /**
     * Obtener un propietario por su ID.
     * @param id el ID del propietario a buscar
     * @return PropietarioResponseDTO con los datos del propietario encontrado
     */
    public PropietarioResponseDTO obtenerPropietarioPorId(Long id) {
        Propietario propietario = propietarioRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Propietario no encontrado"));

        return Mapper.toDTO(propietario);
    }

    /**
     * Vincular un usuario existente a un propietario.
     * @param propietarioId el ID del propietario existente al que se vinculará el
     *                      usuario
     * @param correoUsuario correo electrónico del usuario a vincular
     * @return PropietarioResponseDTO con los datos del propietario actualizado
     */
    public PropietarioResponseDTO vincularUsuario(Long propietarioId, String correoUsuario) {
        Propietario propietario = propietarioRepository.findById(propietarioId)
                .orElseThrow(() -> new NotFoundException("Propietario no encontrado"));

        Usuario usuario = usuarioRepository.findByCorreo(correoUsuario)
                .orElseThrow(() -> new NotFoundException("Usuario no encontrado"));

        propietario.setUsuario(usuario);
        return Mapper.toDTO(propietarioRepository.save(propietario));
    }

    /**
     * Validar el total de incidencias de un propietario.
     * Una vez que el propietario alcanza 3 incidencias, se deshabilita su tarjeta
     * de pase al estacionamiento, hasta que se vuelva a activar de manera manual (de momento seria modificando el campo directamente en la base de datos)
     * @param id el ID del propietario a validar
     */
    public void validarTotalIncidenciasPropietario(Long id) {

        Long incidenciasUsuario = incidenciaRepository.countByAutomovil_Propietario_Id(id);
        if (incidenciasUsuario >= 3) {
            deshabilitarTarjeta(id);
        }
    }

    /**
     * Deshabilitar la tarjeta de pase de un propietario.
     * @param id el ID del propietario cuya tarjeta se deshabilitará
     */
    public void deshabilitarTarjeta(Long id) {
        Propietario propietario = propietarioRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Propietario no encontrado"));

        if (propietario.isTarjetaPase()) {
            propietario.setTarjetaPase(false);
            propietarioRepository.save(propietario);
        }
    }
}
