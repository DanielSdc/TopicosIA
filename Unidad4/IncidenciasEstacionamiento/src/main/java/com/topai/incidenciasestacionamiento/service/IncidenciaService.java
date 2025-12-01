package com.topai.incidenciasestacionamiento.service;

import com.topai.incidenciasestacionamiento.dto.request.IncidenciaRequestDTO;
import com.topai.incidenciasestacionamiento.dto.response.IncidenciaResponseDTO;
import com.topai.incidenciasestacionamiento.exception.NotFoundException;
import com.topai.incidenciasestacionamiento.mapper.Mapper;
import com.topai.incidenciasestacionamiento.model.Automovil;
import com.topai.incidenciasestacionamiento.model.Incidencia;
import com.topai.incidenciasestacionamiento.model.Usuario;
import com.topai.incidenciasestacionamiento.repository.AutomovilRepository;
import com.topai.incidenciasestacionamiento.repository.IncidenciaRepository;
import com.topai.incidenciasestacionamiento.repository.UsuarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Servicio para la gestión de incidencias.
 * Se implementa la logística de negocio relacionada con las incidencias
 * {@link Incidencia}.
 */
@Service
public class IncidenciaService {

        @Autowired
        IncidenciaRepository incidenciaRepository;

        @Autowired
        AutomovilRepository automovilRepository;

        @Autowired
        UsuarioRepository usuarioRepository;

        @Autowired
        PropietarioService propietarioService;

        /**
         * Crear una nueva incidencia.
         * @param dto datos de la incidencia a crear
         * @param correo correo electrónico del usuario que crea la incidencia
         * @return IncidenciaResponseDTO con los datos de la incidencia creada
         */
        public IncidenciaResponseDTO crearIncidencia(IncidenciaRequestDTO dto,
                        String correo) {
                Usuario usuario = usuarioRepository.findByCorreo(correo)
                                .orElseThrow(() -> new NotFoundException("Usuario test no encontrado"));
                Automovil automovil = automovilRepository.findByMatricula(dto.getMatricula())
                                .orElseThrow(() -> new NotFoundException("Vehículo no registrado"));
                LocalDateTime fecha = LocalDateTime.now();

                Incidencia incidencia = Incidencia.builder()
                                .fecha(fecha)
                                .longitud(dto.getLongitud())
                                .latitud(dto.getLatitud())
                                .automovil(automovil)
                                .usuario(usuario)
                                .build();

                Incidencia incidenciaGuardada = incidenciaRepository.save(incidencia);

                propietarioService.validarTotalIncidenciasPropietario(automovil.getPropietario().getId());

                return Mapper.toDTO(incidenciaGuardada);
        }

        /**
         * Obtener las incidencias asociadas a los automóviles de un usuario.
         * @param correo correo electrónico del usuario
         * @return lista de IncidenciaResponseDTO con las incidencias asociadas a los
         *         automóviles del usuario
         */
        public List<IncidenciaResponseDTO> traerIncidenciasDelUsuario(String correo) {
                return incidenciaRepository.findByAutomovil_Propietario_Usuario_Correo(correo)
                                .stream()
                                .map(Mapper::toDTO)
                                .toList();
        }

        /**
         * Obtener las incidencias creadas por un usuario específico.
         * @param correo correo electrónico del usuario
         * @return lista de IncidenciaResponseDTO con las incidencias creadas por el
         *         usuario
         */
        public List<IncidenciaResponseDTO> traerIncidenciasCreadasPorUsuario(String correo) {
                return incidenciaRepository.findByUsuario_Correo(correo)
                                .stream()
                                .map(Mapper::toDTO)
                                .toList();
        }
}
