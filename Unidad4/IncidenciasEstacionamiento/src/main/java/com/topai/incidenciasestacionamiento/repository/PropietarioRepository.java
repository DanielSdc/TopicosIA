package com.topai.incidenciasestacionamiento.repository;

import com.topai.incidenciasestacionamiento.model.Propietario;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PropietarioRepository extends JpaRepository<Propietario, Long> {
}
