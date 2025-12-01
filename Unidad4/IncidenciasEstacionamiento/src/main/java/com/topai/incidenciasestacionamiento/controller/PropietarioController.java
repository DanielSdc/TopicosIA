package com.topai.incidenciasestacionamiento.controller;

import com.topai.incidenciasestacionamiento.dto.request.PropietarioRequestDTO;
import com.topai.incidenciasestacionamiento.dto.response.PropietarioResponseDTO;
import com.topai.incidenciasestacionamiento.service.PropietarioService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.security.Principal;

@RestController
@RequestMapping("/api/propietarios")
public class PropietarioController {

    @Autowired
    private PropietarioService propietarioService;

    @PostMapping
    public ResponseEntity<PropietarioResponseDTO> crearPropietario(
            @Valid @RequestBody PropietarioRequestDTO propietarioRequestDTO) {
        PropietarioResponseDTO propietario = propietarioService.registrarPropietario(propietarioRequestDTO);

        return ResponseEntity.created(URI.create("/api/propietarios/" + propietario.getId())).body(propietario);
    }

    @PostMapping("/{id}/vincular")
    public ResponseEntity<?> vincularUsuario(@PathVariable Long id, Principal principal) {

        propietarioService.vincularUsuario(id, principal.getName());
        return ResponseEntity.ok("Cuenta vinculada con vehiculos");
    }

    @GetMapping("/{id}")
    public ResponseEntity<PropietarioResponseDTO> obtenerPropietario(@PathVariable Long id) {
        return ResponseEntity.ok(propietarioService.obtenerPropietarioPorId(id));
    }
}
