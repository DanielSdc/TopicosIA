package com.topai.incidenciasestacionamiento.service;

import com.topai.incidenciasestacionamiento.dto.request.AutomovilRequestDTO;
import com.topai.incidenciasestacionamiento.dto.response.AutomovilResponseDTO;
import com.topai.incidenciasestacionamiento.exception.NotFoundException;
import com.topai.incidenciasestacionamiento.mapper.Mapper;
import com.topai.incidenciasestacionamiento.model.Automovil;
import com.topai.incidenciasestacionamiento.model.Propietario;
import com.topai.incidenciasestacionamiento.repository.AutomovilRepository;
import com.topai.incidenciasestacionamiento.repository.PropietarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Servicio para la gestión de automóviles.
 * Se implementa la logística de negocio relacionada con los automóviles
 * {@link Automovil}.
 */
@Service
public class AutomovilService {

    @Autowired
    private AutomovilRepository automovilRepository;
    @Autowired
    private PropietarioRepository propietarioRepository;

    /**
     *  registrar un nuevo automóvil.
     * 
     * @param automovilDTO datos del automóvil a registrar
     * @return AutomovilResponseDTO con los datos del automóvil registrado
     */
    public AutomovilResponseDTO registrarAutomovil(AutomovilRequestDTO automovilDTO) {
        Long idPropietario = automovilDTO.getPropietario();

        Propietario propietario = propietarioRepository.findById(idPropietario)
                .orElseThrow(() -> new NotFoundException("El propietario con ID " + idPropietario + " no existe."));

        Automovil automovil = Automovil.builder()
                .matricula(automovilDTO.getMatricula())
                .propietario(propietario)
                .marca(automovilDTO.getMarca())
                .modelo(automovilDTO.getModelo())
                .year(automovilDTO.getYear())
                .build();

        return Mapper.toDTO(automovilRepository.save(automovil));
    }

    /**
     *  Buscar un automóvil por su matrícula.
     * 
     * @param matricula matrícula del automóvil a buscar
     * @return AutomovilResponseDTO con los datos del automóvil encontrado
     */
    public AutomovilResponseDTO buscarPorMatricula(String matricula) {
        Automovil automovil = automovilRepository.findByMatricula(matricula)
                .orElseThrow(
                        () -> new NotFoundException("No se encontró ningún vehiculo con la matricula: " + matricula));
        return Mapper.toDTO(automovil);
    }

    /**
     * Listar los automóviles asociados a un usuario específico.
     * 
     * @param correoUsuario correo electrónico del usuario
     * @return lista de AutomovilResponseDTO con los automóviles asociados al
     *         usuario
     */
    public List<AutomovilResponseDTO> listarAutomoviles(String correoUsuario) {

        List<Automovil> misAutos = automovilRepository.findByPropietario_Usuario_Correo(correoUsuario);

        return misAutos.stream()
                .map(Mapper::toDTO)
                .collect(Collectors.toList());
    }

}
