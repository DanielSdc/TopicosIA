package com.topai.incidenciasestacionamiento.controller;

import com.topai.incidenciasestacionamiento.dto.request.AutomovilRequestDTO;
import com.topai.incidenciasestacionamiento.dto.response.AutomovilResponseDTO;
import com.topai.incidenciasestacionamiento.service.AutomovilService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.security.Principal;
import java.util.List;

@RestController
@RequestMapping("/api/automoviles")
public class AutomovilController {

    @Autowired
    private AutomovilService automovilService;

    @PostMapping
    public ResponseEntity<AutomovilResponseDTO> crearAutomovil (@Valid @RequestBody AutomovilRequestDTO automovilRequestDTO){
        AutomovilResponseDTO automovil = automovilService.registrarAutomovil(automovilRequestDTO);

        return ResponseEntity.created(URI.create("/api/automoviles/"+automovil.getId())).body(automovil);
    }

    @GetMapping("/mis-autos")
    public ResponseEntity<List<AutomovilResponseDTO>> obtenerMisAutomoviles (Principal principal){
        return ResponseEntity.ok(
                automovilService.listarAutomoviles(principal.getName())
        );
    }

    @GetMapping("/{matricula}")
    public ResponseEntity<AutomovilResponseDTO> buscarPorMatricula(@PathVariable String matricula){
        return ResponseEntity.ok(
                automovilService.buscarPorMatricula(matricula)
        );
    }
}
