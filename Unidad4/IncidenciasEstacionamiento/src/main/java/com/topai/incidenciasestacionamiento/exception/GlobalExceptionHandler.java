package com.topai.incidenciasestacionamiento.exception;

import com.topai.incidenciasestacionamiento.dto.response.ErrorResponseDTO;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;

@RestControllerAdvice
public class GlobalExceptionHandler {

    // Este método captura SOLO tus excepciones NotFoundException
    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponseDTO> handleNotFoundException(NotFoundException ex) {

        ErrorResponseDTO errorResponse = new ErrorResponseDTO(
                ex.getMessage(),            // "Vehículo no encontrado"
                LocalDateTime.now(),        // Fecha y hora actual
                HttpStatus.NOT_FOUND.value() // 404
        );

        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }

    // Opcional: Un manejador genérico para cualquier otro error inesperado (NullPointer, etc.)
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponseDTO> handleGlobalException(Exception ex) {

        ErrorResponseDTO errorResponse = new ErrorResponseDTO(
                "Ocurrió un error interno en el servidor: " + ex.getMessage(),
                LocalDateTime.now(),
                HttpStatus.INTERNAL_SERVER_ERROR.value() // 500
        );

        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}