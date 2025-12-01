package com.topai.incidenciasestacionamiento.repository;

import com.topai.incidenciasestacionamiento.model.Incidencia;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface IncidenciaRepository extends JpaRepository<Incidencia, Long> {
    // List<Incidencia> findByUsuarioCorreo(String correo);

    // Obtener las incidencias de los propietarios de los automoviles con su correo
    List<Incidencia> findByAutomovil_Propietario_Usuario_Correo(String correo);
    List<Incidencia> findByUsuario_Correo(String usuarioCorreo);
    // Obtener el total de incidencias de un propietario con su ID
    Long countByAutomovil_Propietario_Id(Long automovilPropietarioId);
}
