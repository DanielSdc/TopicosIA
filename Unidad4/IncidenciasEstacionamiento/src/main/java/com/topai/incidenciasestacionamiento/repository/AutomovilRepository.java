package com.topai.incidenciasestacionamiento.repository;
import java.util.List;
import java.util.Optional;
import com.topai.incidenciasestacionamiento.model.Automovil;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AutomovilRepository extends JpaRepository<Automovil, Long> {

    Optional<Automovil> findByMatricula(String matricula);

    // Obtener los automoviles mediante el correo de un propietario
    List<Automovil> findByPropietario_Usuario_Correo(String correo);
}
